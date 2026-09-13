---
title: "使用 LoRA 微调大语言模型"
title_en: "LLM Finetuning with LoRA"
source: https://sebastianraschka.com/blog/2023/llm-finetuning-lora.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 使用 LoRA 微调大语言模型

> 原文：[LLM Finetuning with LoRA](https://sebastianraschka.com/blog/2023/llm-finetuning-lora.html)

## 核心要点

在快速演进的 AI 领域，高效且有效地使用大语言模型正变得越来越重要。在本文中，你将学习如何以计算高效的方式，用[低秩适应](https://sebastianraschka.com/glossary/#lora "LoRA (Low-Rank Adaptation)")（LoRA）来调优一个大语言模型！

## 为什么要微调？

预训练大语言模型之所以常被称为基础模型（foundation model），是有充分理由的：它们在各种任务上都有良好表现，我们可以把它们作为基础，在目标任务上进行微调。正如我上一篇文章（[《理解大语言模型的参数高效微调：从 Prefix Tuning 到 LLaMA-Adapters》](https://sebastianraschka.com/blog/2023/llm-finetuning-llama-adapter.html)）所讨论的，微调让我们能把模型适配到目标领域和目标任务。尽管如此，它在计算上可能非常昂贵——模型越大，更新其层的代价就越高。

作为更新所有层的替代方案，prefix tuning 和 adapters 等参数高效方法应运而生——详细综述请见我的[上一篇文章](https://sebastianraschka.com/blog/2023/llm-finetuning-llama-adapter.html)。现在，又多了一种流行的参数高效微调技术：[Hu 等人提出的低秩适应（LoRA）](https://arxiv.org/abs/2106.09685)。LoRA 是什么？它如何工作？它与其他流行的微调方法相比又如何？让我们在本文中回答所有这些问题！

## 低秩适应背后的思想

参数高效的*低秩适应*（Low-rank adaptation）微调技术，简而言之，就是针对大型模型权重矩阵的一种隐式低秩变换技术。那么，什么是低秩变换？

其整体思想与概念和主成分分析（PCA）以及奇异值分解（SVD）相关：我们用低维表示来近似一个高维矩阵或数据集。换句话说，我们试图在原始特征空间（或矩阵）中，找到少数几个维度的（线性）组合，使其能够捕捉数据集中的大部分信息。

![Llm finetuning lora pca](https://sebastianraschka.com/images/blog/2023/llm-finetuning-lora/pca.webp)

## 让权重更新更高效

在上述思想的基础上，论文 [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) 提出把权重变化 *ΔW* 分解为更低秩的表示。（严格来说，LoRA 并不直接对矩阵做分解，而是通过反向传播学习得到分解后的矩阵——这是一个细节问题，后文会讲清楚它为什么重要。）

在深入考察 LoRA 之前，我们先简要说明常规微调过程中的训练流程。那么，权重变化 *ΔW* 是什么？假设 *W* 表示某个神经网络层的权重矩阵，那么通过常规反向传播，我们可以得到权重更新 *ΔW*，它通常按损失对权重的负梯度乘以学习率来计算：

\(\Delta W = \alpha ( -\nabla L\_W)\)。

随后，当我们得到 *ΔW*，就可以按如下方式更新原始权重：\(W' = W + \Delta W\)。下图展示了这一过程（为简单起见，省略了偏置向量）：

或者，我们也可以把权重更新矩阵单独保留，并按如下方式计算输出：\(h = W x + \Delta W x,\)

![Llm finetuning lora regular finetuning](https://sebastianraschka.com/images/blog/2023/llm-finetuning-lora/regular-finetuning.webp)

其中 \(x\) 表示输入，如下图所示。

![Llm finetuning lora regular finetuning alt](https://sebastianraschka.com/images/blog/2023/llm-finetuning-lora/regular-finetuning-alt.webp)

我们为什么要这么做？就目前而言，这种替代形式是为了教学目的、用于说明 LoRA，但我们后面还会回到它。

当我们训练神经网络中的全连接（即"稠密"）层时，如上所示，权重矩阵通常是满秩的——这是一个术语，意思是矩阵不含有任何线性相关（即"冗余"）的行或列。与满秩相对，低秩意味着矩阵含有冗余的行或列。

因此，虽然[预训练模型](https://sebastianraschka.com/glossary/#base-model "Base Model")的权重在预训练任务上是满秩的，但 LoRA 的作者指出，根据 [Aghajanyan 等人](https://arxiv.org/abs/2012.13255)（2020）的研究，预训练大语言模型在被适配到新任务时具有较低的"内在维度"（intrinsic dimension）。

内在维度低意味着数据可以在保留大部分关键信息或结构的同时，被低维空间有效表示或近似。换句话说，这意味着我们可以把适配新任务后的新权重矩阵分解成低维（更小）的矩阵，而不会丢失太多重要信息。

举例来说，假设 \(\Delta W\) 是权重矩阵 \(W \in \mathbb{R}^{A \times B}\) 的权重更新，那么我们可以把权重更新矩阵分解为两个更小的矩阵：\(\Delta W = W\_A W\_B\)，其中 \(W\_A \in \mathbb{R}^{A \times r}\)，\(W\_B \in \mathbb{R}^{r \times B}.\) 在这里，我们保持原始权重 \(W\) 冻结，只训练新矩阵 \(W\_A\) 和 \(W\_B\)。简而言之，这就是 LoRA 方法，如下图所示。

![Llm finetuning lora lora weights](https://sebastianraschka.com/images/blog/2023/llm-finetuning-lora/lora-weights.webp)

### 选择秩

注意，上图中的 \(r\) 是一个超参数，我们可以用它来指定用于适配的低秩矩阵的秩。较小的 \(r\) 意味着更简单的低秩矩阵，从而在适配过程中需要学习的参数更少。这可以带来更快的训练速度，并可能降低计算需求。然而，\(r\) 越小，低秩矩阵捕捉任务特定信息的能力就越弱。这可能导致适配质量下降，模型在新任务上的表现可能不如较大的 \(r\)。总结一下，在 LoRA 中选择较小的 \(r\) 需要在模型复杂度、适配能力与欠拟合或过拟合风险之间做出权衡。因此，重要的是尝试不同的 \(r\) 取值，找到恰当的平衡，以在新任务上取得理想性能。

### 实现 LoRA

LoRA 的实现相当直接。我们可以把它看作对大语言模型中全连接层的一次修改版前向传播。用伪代码表示如下：

```python
input_dim = 768  # e.g., the hidden size of the pre-trained model
output_dim = 768  # e.g., the output size of the layer
rank = 8  # The rank 'r' for the low-rank adaptation

W = ... # from pretrained network with shape input_dim x output_dim

W_A = nn.Parameter(torch.empty(input_dim, rank)) # LoRA weight A
W_B = nn.Parameter(torch.empty(rank, output_dim)) # LoRA weight B

# Initialization of LoRA weights
nn.init.kaiming_uniform_(W_A, a=math.sqrt(5))
nn.init.zeros_(W_B)

def regular_forward_matmul(x, W):
    h = x @ W
return h

def lora_forward_matmul(x, W, W_A, W_B):
    h = x @ W  # regular matrix multiplication
    h += x @ (W_A @ W_B) * alpha # use scaled LoRA weights
return h
```

在上面的伪代码中，`alpha` 是一个缩放因子，用于调整组合结果（原始模型输出加上低秩适应）的幅度。它在预训练模型的知识与新的任务特定适配之间取得平衡——默认情况下，`alpha` 通常设为 1。另外注意，\(W\_A\) 被初始化为较小的随机权重，而 \(W\_B\) 被初始化为 0，因此在训练开始时

\(\Delta W = W\_A W\_B = 0\)，也就是说我们从原始权重出发开始训练。

### 参数效率

现在，我们来谈谈那个显而易见的问题：既然引入了新的权重矩阵，这怎么就算参数高效了呢？新的矩阵 \(W\_A\) 和 \(W\_B\) 可以非常小。例如，假设 \(A=100\)、\(B=500\)，那么 \(\Delta W\) 的大小为 \(100 \times 500 = 50,000\)。而如果我们把它分解为两个更小的矩阵 \(W\_A \in \mathbb{R}^{100 \times 5}\) 和 \(W\_B \in \mathbb{R}^{5 \times 500}\)，参数总量只有 \(5\times 100 + 5 \times 500 = 3,000\) 个。

### 降低推理开销

注意，在实践中，如果训练结束后我们像上面那样把原始权重 \(W\) 与矩阵 \(W\_A\)、\(W\_B\) 分开保留，推理时会有轻微的效率损失，因为这引入了额外的计算步骤。作为替代，我们可以在训练后通过 \(W' = W + W\_A W\_B\) 来更新权重，这与前文提到的 \(W' = W + \Delta W\) 类似。

不过，把权重矩阵 \(W\_A\) 和 \(W\_B\) 分开保留也有实际好处。例如，设想我们想把预训练模型作为多个客户共用的基座模型，并且希望从这个基座模型出发，为每个客户分别创建一个微调后的大语言模型。在这种情况下，我们不需要为每个客户存储完整的权重矩阵 \(W'\)——对一个模型来说，存储全部权重 \(W' = W + W\_A W\_B\) 在大语言模型的场景下可能非常庞大，因为大语言模型通常拥有数十亿乃至数万亿的权重参数。所以，我们只需保留原始模型 \(W\)，并只存储新的轻量级矩阵 \(W\_A\) 和 \(W\_B\) 即可。

用具体数字来说明这一点：一个完整的 7B LLaMA 检查点需要 23 GB 的存储空间，而如果我们选择秩 \(r=8\)，LoRA 权重可以小到只有 8 MB。

### 实际效果如何？

LoRA 在实践中的表现如何？与全量微调以及其他参数高效方法相比又如何？根据 [LoRA 论文](https://arxiv.org/abs/2106.09685)，在多个任务特定基准测试上，使用 LoRA 的模型的建模性能略优于使用 [Adapters](https://arxiv.org/abs/2110.07280)、[prompt tuning](https://arxiv.org/abs/2104.08691) 或 [prefix tuning](https://arxiv.org/abs/2101.00190) 的模型。而且 LoRA 的表现常常甚至优于微调所有层，如下面这张来自 LoRA 论文、加了标注的表格所示。（ROUGE 是一种用于评估语言翻译性能的指标，我在[这里](https://twitter.com/rasbt/status/1639625228622917632?s=20)做了更详细的解释。）

![Llm finetuning lora lora table 2](https://sebastianraschka.com/images/blog/2023/llm-finetuning-lora/lora-table-2.webp)

这里值得一提的是，LoRA 与其他微调方法是正交的，也就是说，它还可以与 prefix tuning、adapters 等方法组合使用。

## LoRA 与 LLaMA

现在，让我们使用 LoRA 的一个具体实现来微调 Meta 的热门 LLaMA 模型。由于本文已经很长，我不会在正文中贴出详细代码，但我推荐去看看 [Lit-LLaMA 仓库](https://github.com/Lightning-AI/lit-llama)，它是 Meta 的热门 LLaMA 模型的一个简洁、易读的重实现。

除了训练和运行 LLaMA 本身的代码（使用 Meta 原版 LLaMA 权重）之外，它还包含使用 [LLaMA-Adapter](https://github.com/Lightning-AI/lit-llama/blob/main/finetune_adapter.py) 和 [LoRA](https://github.com/Lightning-AI/lit-llama/blob/main/finetune_lora.py) 微调 LLaMA 的代码。

作为入门，我推荐以下*操作指南*文件：

1. 下载预训练权重 [ [download\_weights.md](https://github.com/Lightning-AI/lit-llama/blob/main/howto/download_weights.md) ]
2. 用 LoRA 微调 [ [finetune\_lora.md](https://github.com/Lightning-AI/lit-llama/blob/main/howto/finetune_lora.md) ]
3. 用 Adapter 微调 [ [finetune\_adapter.md](https://github.com/Lightning-AI/lit-llama/blob/main/howto/finetune_adapter.md) ]（可选，用于对比研究）

在下一节中，我们将比较 7B LLaMA 基座模型与分别用 LoRA 和 LLaMA-Adapter 微调后的 7B LLaMA 基座模型。（注意，这需要一块显存至少 24 GB 的 GPU。）（关于 LLaMA-Adapter 方法的更多细节，请见我的[上一篇文章](https://sebastianraschka.com/blog/2023/llm-finetuning-llama-adapter.html)）

## LoRA-LLaMA 计算性能基准测试

在本节中，我们将比较 LLaMA 7B 基座模型与分别使用 LoRA 和 LLaMA-Adapter 微调后的基座模型的计算性能。

微调所用数据集是[这里](https://github.com/tatsu-lab/stanford_alpaca#data-release)描述的 Alpaca 52k 指令数据集，它具有如下结构：

![Llm finetuning lora alpaca instruct](https://sebastianraschka.com/images/blog/2023/llm-finetuning-lora/alpaca-instruct.webp)

该数据集本身是按照 [Self-Instruct 论文](https://arxiv.org/abs/2212.10560)中描述的方法生成的，由 49,759 个训练样本和 2000 个验证样本组成。Self-Instruct 流程可以概括为 4 个步骤：

它是如何工作的？简而言之，这是一个 4 步流程：

1. 用一组人工编写的指令（本例中为 175 条）作为种子任务池，并从中采样指令
2. 使用一个预训练大语言模型（如 GPT-3）来确定任务类别
3. 给定新指令，让预训练大语言模型生成响应
4. 对响应进行收集、修剪和过滤，然后加入任务池

![Llm finetuning lora self instruct](https://sebastianraschka.com/images/blog/2023/llm-finetuning-lora/self-instruct.webp)

注意，Alpaca 52k 数据集就是通过上述自动化 self-instruct 流程收集的。不过，你也可以使用另一个数据集（或与它进行对比）。例如，一个有趣的候选是最近发布的开源 [databricks-dolly-15k](https://github.com/databrickslabs/dolly/tree/master/data) 数据集，它包含约 1.5 万条由 Databricks 员工撰写的指令/响应微调记录。如果你想用这个 Dolly 15k 数据集替代 Alpaca 52k 数据集，Lit-LLaMA 仓库中提供了一个数据集准备脚本。

在以下超参数设置（block size、batch size 和 LoRA r）下，Adapter 与 LoRA 都能使用 bfloat-16 [混合精度](https://sebastianraschka.com/glossary/#mixed-precision "Mixed Precision")训练，在单块 24 GB 显存的 GPU 上微调 7B 参数的 LLaMA 基座模型。

### LoRA

```python
learning_rate = 3e-4
batch_size = 128
micro_batch_size = 4
gradient_accumulation_steps = batch_size // micro_batch_size
epoch_size = 50000  # train dataset size
num_epochs = 5
max_iters = num_epochs * epoch_size // micro_batch_size // devices
weight_decay = 0.0
block_size = 512
lora_r = 8
lora_alpha = 16
lora_dropout = 0.05
warmup_steps = 100
```

### LLaMA Adapter

```python
learning_rate = 9e-3
batch_size = 128 / devices
micro_batch_size = 4
gradient_accumulation_steps = batch_size // micro_batch_size
epoch_size = 50000  # train dataset size
num_epochs = 5
max_iters = num_epochs * epoch_size // micro_batch_size // devices
weight_decay = 0.02
block_size = 512
warmup_steps = epoch_size * 2 // micro_batch_size // devices
```

### 全量微调

```python
learning_rate = 3e-5
batch_size = 128 / devices
micro_batch_size = 4
gradient_accumulation_steps = batch_size // micro_batch_size
epoch_size = 50000  # train dataset size
num_epochs = 5
max_iters = num_epochs * epoch_size // micro_batch_size // devices
weight_decay = 0.0
block_size = 512
warmup_steps = 100
```

以防将来代码发生变化，我把代码（连同超参数设置）放在了 [GitHub 的这里](https://github.com/rasbt/low-rank-adaptation-blog)。

Adapter 大约使用了 22 GB 显存，在 A100 上用时 162 分钟完成了 62,400 次迭代。LoRA 使用了 21 GB 显存，用时 192 分钟。总体而言，基于 Lit-LLaMA 的实现，Adapter 与 LoRA 占用的内存大致相同，训练时间也大致相当。（注意，这是在单 GPU 上的结果；如果你有多块 GPU，只需把 `devices` 参数改为大于 1，即可利用额外的加速！）

作为对比，全量微调（LLaMA 7B 由 32 个 transformer 块和 3 个全连接输出层组成）至少需要 2 块显存不少于 30 GB 的 GPU，并进行全分片训练来分布权重。另一种选择是使用 4 块 GPU，每块 GPU 的最大显存占用为 22 GB。在 4 块 GPU 上的训练耗时 1956 分钟。若在单 GPU 上，则至少需要 6,000 分钟，成本将达到参数高效的 LLaMA-Adapter 或 LoRA 方案的 30–40 倍。

接下来，让我们看看应用不同微调策略之后的模型输出。

## 评估建模性能

评估大语言模型生成文本的指标有若干种。例如，[困惑度](https://sebastianraschka.com/glossary/#perplexity "Perplexity")（perplexity）、BLEU 和 ROUGE 分数是自然语言处理中最常用的几种评估指标，用于衡量大语言模型在各类任务上的表现。然而，所有这些指标都有明显的不足，人工评估仍然是黄金标准——而人工评估的缺点是成本高昂且难以自动化。由于本文已经非常长，我不打算详细讨论模型评估方法，而是把这个话题留待未来单独成文。在那篇后续文章中，我们会考察不同的问答数据集（包括 [`wikitext`](https://paperswithcode.com/dataset/wikitext-2)、[`c4`](https://paperswithcode.com/dataset/c4) 和 [`ptb`](https://catalog.ldc.upenn.edu/docs/LDC95T7/treebank2.index.html)，以及上文提到的那些指标）。所以，为了简单起见，下面我们只做定性的模型比较，看看各个模型生成的一些输出。

## 定性比较

为了对模型进行定性比较，我们将使用提示词 `"Please explain how weight decay works"`

**基座模型**

```python
$ python generate.py --checkpoint_path checkpoints/lit-llama/7B/lit-llama.pth
```

> *Please explain how weight decay works…and why it sometimes seems to work and sometimes doesn’t!*
>
> *In the simplest terms, weight decay removes features from the model (as a function of how important they are). It is also known as regularization.*
>
> *Regularization has*
>
> Time for inference 1: 4.18 sec total, 11.95 tokens/sec
>
> Memory used: 13.54 GB

可以看到，模型在续写提示词时先补上了"…and why it sometimes seems to work and sometimes doesn't!"。这是因为基座模型只在下一词预测任务上训练过，并没有被专门训练来遵循指令。尽管如此，它在下面还是尝试给出了解释。这个解释关于正则化的表述大体正确，但并没有真正抓住权重衰减的关键机制。（公平起见，应当说明：出于效率考虑，训练集的输入长度被限制在了 256 个 token 以内。）

### LLaMA-Adapter

```python
$ python generate_adapter.py --adapter_path out/adapter/alpaca/lit-llama-adapter-finetuned.pth --pretrained_path checkpoints/lit-llama/7B/lit-llama.pth
```

> *Weight decay is a way to penalize terms for their word-count. By choosing sentences with fewer words, a model is more likely to select those sentences, which may provide important information.*
>
> Time for inference: 7.04 sec total, 14.21 tokens/sec
>
> Memory used: 13.56 GB

这个解释在语法上没有问题，但同样未必是我们想要的内容。

### LoRA

```python
$ python generate_lora.py --lora_path out/lora/alpaca/lit-llama-lora-finetuned.pth --pretrained_path checkpoints/lit-llama/7B/lit-llama.pth
```

> *Weight decay is an algorithm parameter used in machine learning models to reduce overfitting. It is a process where the weights of the model are adjusted in order to decrease the influence of less-important features in the model and prevent overfitting. Weight decay is used by adding a small amount of noise to the weights to reduce the impact of the model on the training data. This process encourages the model to focus more on the features that are more important to the predictive task.*
>
> Time for inference: 3.25 sec total, 30.76 tokens/sec
>
> Memory used: 27.65 GB

我们越来越接近了；当我们想到广义线性模型——即强迫模型学习与输入特征相乘的更小的权重参数——时，这个解释是说得通的。而在神经网络中，这通常会施加于模型中的所有权重参数。

注意，上面的 LoRA 方法目前占用的内存最多。不过，我们可以通过把 LoRA 权重与预训练模型权重合并来降低这一内存占用，如前文所述。

这份定性概览只是这几个模型能力的一个小小切面，因为评估大语言模型本身就是一个大话题。我们将在未来的文章中更详细地回顾这个话题。但就本文的要点而言：LoRA 可以以相对划算的方式，在一个指令数据集上微调大语言模型。

## 结论

在本文中，我们讨论了低秩适应（LoRA），一种参数高效的全量微调替代方案。我们看到，使用 LoRA 微调 LLaMA 这样相对较大的模型，可以在单块 GPU 上于几个小时内完成，这对那些不愿在 GPU 资源上花费数千美元的人来说尤其有吸引力。LoRA 特别好用的一点是，我们可以选择把新的 LoRA 权重矩阵与原始预训练权重合并，从而在推理时不引入额外的开销或复杂性。

随着 ChatGPT 或 GPT-4 的开源替代品越来越多，在各种研究领域和行业中，在特定目标数据集或目标上微调并定制这些大语言模型将变得越来越有吸引力。而 LoRA 这类参数高效微调技术让微调更加节省资源、更加触手可及。

[Lit-LLaMA 仓库](https://github.com/Lightning-AI/lit-llama)提供了 LoRA 与 LLaMA-Adapter 等参数高效微调技术。如果你对扩展或其他替代技术有想法，我们随时欢迎贡献与建议。请随时通过 [GitHub](https://github.com/Lightning-AI/lit-llama) 或 [Discord](https://discord.com/invite/XncpTy7DSt) 与我们联系。

**致谢**

我要感谢 Luca Antiga 和 Adrian Waelchli 为提高本文清晰度提出的建设性反馈。
