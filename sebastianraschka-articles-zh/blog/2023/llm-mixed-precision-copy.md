---
title: "大语言模型的混合精度技术"
title_en: "Mixed-Precision Techniques for LLMs"
source: https://sebastianraschka.com/blog/2023/llm-mixed-precision-copy.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 大语言模型的混合精度技术

> 原文：[Mixed-Precision Techniques for LLMs](https://sebastianraschka.com/blog/2023/llm-mixed-precision-copy.html)

训练和使用大语言模型（LLM）代价高昂，因为它们的计算需求和内存占用都很大。本文将探讨如何利用较低精度的格式将训练和推理速度提升至 3 倍，同时不损害模型的准确率。

虽然我们的主要焦点是大语言模型的例子，但这些技术中的大多数相当通用，同样适用于其他深度学习架构。

## 理解混合精度训练

混合精度训练是让我们在现代 GPU 上显著提升训练速度的关键技术之一。有时，这可以带来 2 到 3 倍的加速！让我们看看它是如何工作的。

### 使用 32 位精度

在 GPU 上训练深度神经网络时，我们通常使用低于最高档位的精度，即 32 位浮点运算（事实上，PyTorch 默认使用的就是 32 位浮点数）。

相比之下，在传统科学计算中，我们通常使用 64 位浮点数。一般来说，位数越多对应着越高的精度，从而降低计算过程中误差累积的几率。因此，64 位浮点数（也称为双精度）长期以来一直是科学计算的标准，因为它能以更高的准确度表示大范围的数值。

然而，在深度学习中，使用 64 位浮点运算被认为是不必要的且计算上代价高昂，因为 64 位运算通常更昂贵，而且 GPU 硬件也没有针对 64 位精度做优化。因此，32 位浮点运算（也称为单精度）成了在 GPU 上训练深度神经网络的标准。

在浮点数的语境中，"位"指的是计算机内存中用于表示数字的二进制位。用于表示数字的位数越多，精度就越高，可表示的数值范围也越大。在浮点表示中，数字由三个部分组合存储：符号、指数和尾数（或称有效数字）。

![Llm mixed precision copy 32 bit](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/32-bit.webp)

在浮点数中，数值表示为尾数、底数的指数次幂与符号三者的乘积。尾数与小数点后的数字相关但不等同。如果你对确切的公式感兴趣（下图中有示意），[我推荐 Wikipedia 上的精彩章节](https://en.wikipedia.org/wiki/Single-precision_floating-point-format)。不过为了方便，我们可以把尾数看作"分数"或"小数值"。

![Llm mixed precision copy half detailed](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/half-detailed.webp)

那么，回到使用较低精度的动机上来，在 GPU 上训练深度神经网络时，32 位浮点运算之所以优于 64 位，本质上主要有两个原因：

1. **减少内存占用。**使用 32 位浮点数的主要优势之一是它们所需的内存是 64 位浮点数的一半。这使得 GPU 内存的利用更高效，从而能够训练更大的模型（以及使用更大的批大小）。
2. **提高计算能力和速度。**由于 32 位浮点运算所需的内存更少，GPU 可以更快地处理它们，从而缩短训练时间。这种加速在深度学习中至关重要，因为训练复杂模型可能需要数天甚至数周。

### 从 32 位精度到 16 位精度

既然已经讨论了 32 位浮点数的好处，我们能不能更进一步？当然可以！最近，混合精度训练已成为一种常见的训练方案，其中我们临时使用 16 位精度进行浮点计算，这通常被称为"半"精度（half precision）。

![Llm mixed precision copy half](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/half.webp)

如上图所示，float16 的指数比 float32 少用 3 位，小数值部分少用 13 位。

但在讨论混合精度训练的机制之前，让我们把不同位精度级别之间的差异变得更直观、更具体。考虑下面这个 PyTorch 代码示例：

```python
>>> import torch
>>> torch.set_printoptions(precision=60)
>>> torch.tensor(1/3, dtype=torch.float64)
tensor(0.333333333333333314829616256247390992939472198486328125000000,
       dtype=torch.float64)
>>> torch.tensor(1/3, dtype=torch.float32)
tensor(0.333333343267440795898437500000000000000000000000000000000000)
>>> torch.tensor(1/3, dtype=torch.float16)
tensor(0.333251953125000000000000000000000000000000000000000000000000,
       dtype=torch.float16)
```

上面的代码示例表明，精度越低，小数点后能看到的准确数字就越少。

深度学习模型对较低精度的算术通常具有鲁棒性。在大多数情况下，用 32 位浮点数代替 64 位浮点数带来的轻微精度下降并不会显著影响模型的预测性能，使得这种权衡是值得的。然而，当我们降到 16 位精度时，事情可能变得棘手。你可能注意到，由于不精确、数值上溢或下溢，损失可能变得不稳定或无法收敛。

上溢（overflow）和下溢（underflow）指的是某些数字超出精度格式所能处理的范围的问题，例如下面所示：

```python
>>> torch.tensor(10**6, dtype=torch.float32)
tensor(1000000.)
>>> torch.tensor(10**6, dtype=torch.float16)
tensor(inf, dtype=torch.float16)
```

顺便说一下，虽然上面的代码片段给出了关于不同精度类型的一些上手示例，你也可以通过 `[torch.finfo](<https://pytorch.org/docs/stable/type_info.html>)` 直接访问数值属性，如下所示：

```python
>>>torch.finfo(torch.float32)

finfo(resolution=1e-06, min=-3.40282e+38, max=3.40282e+38, 
eps=1.19209e-07, smallest_normal=1.17549e-38, 
tiny=1.17549e-38, dtype=float32)

>>> torch.finfo(torch.float16)

finfo(resolution=0.001, min=-65504, max=65504, 
eps=0.000976562, smallest_normal=6.10352e-05, 
tiny=6.10352e-05, dtype=float16)
```

上面的代码显示，最大的 float32 数值是 340,282,000,000,000,000,000,000,000,000,000,000,000（通过 `max`）；例如，float16 数值不能超过 65,504。

所以，在这一节中，我们论证了在现代深度学习中使用"混合精度"训练而非 16 位精度训练的理由。但混合精度训练究竟是如何工作的？为什么它被称为"混合"精度训练，而不只是 16 位精度训练？让我们在下一节中回答这些问题。

### 混合精度训练的机制

它之所以被称为"混合"精度而不是"低"精度训练，是因为我们不会把*所有*参数和运算都转移到 16 位浮点数上。相反，我们在训练期间在 32 位和 16 位运算之间切换，因此得名"混合"精度。

如下图所示，混合精度训练包括：把权重转换为较低精度（FP16）以加快计算、计算梯度、把梯度转换回较高精度（FP32）以保证数值稳定性，以及用缩放后的梯度更新原始权重。

![Llm mixed precision copy mixed training](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/mixed-training.webp)

这种方法在保持神经网络的准确率和稳定性的同时实现了高效训练。

更详细地说，步骤如下。

1. 把权重转换为 FP16：在这一步中，神经网络初始为 FP32 格式的权重（或参数）被转换为较低精度的 FP16 格式。这减少了内存占用并允许更快的计算，因为 FP16 运算所需的内存更少，硬件处理起来也更快。
2. 计算梯度：神经网络的前向和反向传播使用较低精度的 FP16 权重执行。这一步计算损失函数相对于网络权重的梯度（偏导数），它们用于在优化过程中更新权重。
3. 把梯度转换为 FP32：在以 FP16 计算梯度之后，它们被转换回较高精度的 FP32 格式。这一转换对于保持数值稳定性、避免使用较低精度算术时可能出现的梯度消失或爆炸等问题至关重要。
4. 乘以学习率并更新权重：现在是 FP32 格式的梯度会乘以一个学习率（一个决定优化过程中步长大小的标量值）。
5. 然后用第 4 步的乘积来更新原始的 FP32 神经网络权重。学习率有助于控制优化过程的收敛，对取得良好性能至关重要。

上面的流程听起来相当复杂，但在实践中实现起来非常简单。在下一节中，我们将看到如何只改变一行代码，就为微调一个 LLM 而使用混合精度训练。

## 混合精度代码示例

[使用 PyTorch 的 `autocast` 上下文管理器](https://pytorch.org/docs/stable/notes/amp_examples.html)，混合精度训练幸运地并不复杂。此外，借助面向 PyTorch 的开源 [Fabric](https://lightning.ai/docs/fabric/stable/) 库，在常规训练与混合精度训练之间切换变得更加容易，只需要改变一行代码。（由于无需手动干预或修改训练代码，这也常被称为*自动*混合精度训练。）

所以，首先，我们将在运行时间、预测准确率和内存需求方面，考察一个为监督分类任务微调的编码器 LLM（这里是：用于对影评做情感分类的 DistilBERT）。具体来说，我们将微调 transformer 的所有层。关于不同微调类型的更多信息，请参阅我之前的[《理解大语言模型的参数高效微调》](https://lightning.ai/pages/community/article/understanding-llama-adapters/)文章和 [Unit 8.7, A Large Language Model for Classification](https://lightning.ai/pages/courses/deep-learning-fundamentals/unit-8.0-natural-language-processing-and-large-language-models/8.7-a-large-language-model-for-classification/)，或我的免费 Deep Learning Fundamentals 课程。

稍后，我们还将看到不同精度级别的选择对 LLaMA 这类大语言模型的影响。

### **微调基准测试**

让我们从以常规方式、用 float32 位精度（PyTorch 的默认设置）微调 DistilBERT 模型的代码开始：

```python
from datasets import load_dataset
from lightning import Fabric
import torch
from torch.utils.data import DataLoader
import torchmetrics
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

##########################
### 1 Loading the Dataset
##########################

# ... omitted for brevity

#########################################
### 2 Tokenization and Numericalization
#########################################

# ... omitted for brevity

#########################################
### 3 Set Up DataLoaders
#########################################

# ... omitted for brevity

#########################################
### 4 Initializing the Model
#########################################

fabric = Fabric(accelerator="cuda", devices=1)
fabric.launch()

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2)

optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)

model, optimizer = fabric.setup(model, optimizer)
train_loader, val_loader, test_loader = fabric.setup_dataloaders(
    train_loader, val_loader, test_loader)

#########################################
### 5 Finetuning
#########################################

start = time.time()
train(
    num_epochs=3,
    model=model,
    optimizer=optimizer,
    train_loader=train_loader,
    val_loader=val_loader,
    fabric=fabric
)

#########################################
### 6 Evaluation
#########################################

# ... omitted for brevity

print(f"Time elapsed {elapsed/60:.2f} min")
print(f"Memory used: {torch.cuda.max_memory_reserved() / 1e9:.02f} GB")
print(f"Test accuracy {test_acc.compute()*100:.2f}%")
```

上面的代码为节省篇幅做了缩略，但你可以在 GitHub 上的[这里](https://github.com/rasbt/LLM-finetuning-scripts/blob/main/conventional/distilbert-movie-review/mixed-precision-experiment/float32-regular.py)访问完整的代码示例。

在单个 A100 GPU 上训练的结果如下：

```python
Python implementation: CPython
Python version       : 3.9.16

torch       : 2.0.0
lightning   : 2.0.2
transformers: 4.28.1
Torch CUDA available? True

...

Train acc.: 97.28% | Val acc.: 89.88%
Time elapsed 21.75 min
Memory used: 5.37 GB
Test accuracy 89.92%
```

现在，为了与 float16 混合精度训练进行比较，我们只需要改变一行代码，从

```python
fabric = Fabric(accelerator="cuda", devices=1)
```

改为

```python
fabric = Fabric(accelerator="cuda", devices=1, precision="16-mixed")
```

结果如下：

```python
Train acc.: 97.39% | Val acc.: 92.21%
Time elapsed 7.25 min
Memory used: 4.31 GB
Test accuracy 92.15%
```

从上面可以看到，所需的内存减少了，这可能是在 16 位精度下执行矩阵乘法的结果。此外，训练速度提升了约 3 倍，这是非常可观的。

一个有趣而出乎意料的观察是，预测准确率也提高了。一个可能的解释是，这源于使用较低精度带来的正则化效应。较低的精度可能在训练过程中引入一定程度的噪声，这有助于模型更好地泛化并减少过拟合，从而可能提高在验证集和测试集上的准确率。

出于好奇，我们还要添加常规（非混合）float16 训练的结果，通过

```python
fabric = Fabric(accelerator="cuda", devices=1, precision="16-mixed")
```

（注意，这目前需要通过 `pip install git+https://github.com/Lightning-AI/lightning@master` 从最新的开发者分支安装 Lightning。）

遗憾的是，这会导致损失无法收敛，因此准确率等同于在该数据集上随机预测的水平（50%）。

```python
Epoch: 0003/0003 | Batch 2700/2916 | Loss: nan
Epoch: 0003/0003 | Train acc.: 49.86% | Val acc.: 50.80%
Time elapsed 5.23 min
Memory used: 2.87 GB
Test accuracy 50.08%
```

上面的结果总结在下面的图表中：

![Llm mixed precision copy chart1](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/chart1.webp)

如我们所见，float16 混合精度几乎与纯 float16 精度训练一样快（后者在这里存在数值问题），并且预测性能也优于 float32，这可能是由于上文讨论的正则化效应。

### Tensor Core 与矩阵乘法精度

顺便说一下，如果你在支持 Tensor Core 的 GPU 上运行前面的代码，你可能已经在终端中通过 PyTorch 看到过如下消息：

```python
You are using a CUDA device ('NVIDIA A100-SXM4-40GB') that has Tensor Cores. 
To properly utilize them, you should 
set `torch.set_float32_matmul_precision('medium' | 'high')` 
which will trade-off precision for performance. 
For more details, 
read <https://pytorch.org/docs/stable/generated/torch>.
set_float32_matmul_precision.html#torch.set_float32_matmul_precision
```

所以，默认情况下，PyTorch 对矩阵乘法使用"highest"（最高）精度。但如果我们想用更多精度换取性能（如[此处 PyTorch 文档](https://pytorch.org/docs/stable/generated/torch.set_float32_matmul_precision.html)所述），你也可以设置

```python
torch.set_float32_matmul_precision("high")
```

或

```python
torch.set_float32_matmul_precision("medium")
```

（默认通常是"highest"。）

上面的设置将使用 [bfloat16](https://sebastianraschka.com/glossary/#bfloat16 "bfloat16") 数据类型进行矩阵乘法，它是 float16 的一种特殊变体——关于 bfloat16 类型的更多细节见下一节。所以，换句话说，如果你的 GPU 支持 Tensor Core，使用 `torch.set_float32_matmul_precision("high"/"medium")` 将（通过矩阵乘法）隐式启用一种[混合精度](https://sebastianraschka.com/glossary/#mixed-precision "Mixed Precision")训练。

这对结果有什么影响？让我们看看：

![Llm mixed precision copy tensor cores](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/tensor-cores.webp)

所以，正如我们在上面看到的，对于 float32 精度，降低矩阵乘法精度有显著效果：计算性能提升 2.5 倍，内存需求减半。此外，预测准确率也有所提高，这很可能是前面提到的较低精度正则化效应所致。

事实上，使用较低矩阵乘法精度的 float32 训练在性能上几乎与 float16 混合精度训练相当。此外，为 float16 启用较低的矩阵乘法精度并不会改善结果，因为 float16 混合精度训练本身就已经在使用 float16 精度做矩阵乘法了。

### Brain Floating Point（脑浮点数）

另一种浮点格式最近流行了起来，即 [Brain Floating Point](https://cloud.google.com/tpu/docs/bfloat16)（bfloat16，脑浮点数）。Google 为机器学习和深度学习应用开发了这种格式，特别是在其张量处理单元（TPU）中。与常规 float16 格式相比，bfloat16 以降低精度为代价扩展了动态范围。

![Llm mixed precision copy bfloat16](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/bfloat16.webp)

扩展的动态范围帮助 bfloat16 表示非常大和非常小的数字，使其更适合可能遇到大范围数值的深度学习应用。然而，较低的精度可能影响某些计算的准确性，或在某些情况下导致舍入误差。但在大多数深度学习应用中，这种降低的精度对建模性能的影响微乎其微。

虽然 bfloat16 最初是为 TPU 开发的，但现在一些 NVIDIA GPU 也支持这种格式，从属于 NVIDIA Ampere 架构的 A100 Tensor Core GPU 开始。

你可以通过以下代码检查你的 GPU 是否支持 `bfloat16`：

```python
>>> torch.cuda.is_bf16_supported()
True
```

bfloat16 能给我们带来更多好处吗？为了回答这个问题，让我们把之前 DistilBERT 代码以 bfloat16 运行的结果也加进来，只需把一行代码从

```python
fabric = Fabric(accelerator="cuda", devices=1, precision="16-mixed")
```

改为

```python
fabric = Fabric(accelerator="cuda", devices=1, precision="bf16-mixed")
```

（[完整脚本可在 GitHub 上这里获取。](https://github.com/rasbt/LLM-finetuning-scripts/tree/main/conventional/distilbert-movie-review/mixed-precision-experiment)）

为完整起见，我还要添加 float64 运行的结果。另外为了好玩，我们也试试常规（非混合精度）的 bfloat16 训练：

![Llm mixed precision copy chart bfloat](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/chart-bfloat.webp)

有趣的是，float64 在这里取得了比 float32 更高的准确率，这与我们之前关于较低精度对该模型具有正则化效应的论点相矛盾。不过，有意思的一点是，在预测性能方面，Bfloat16 混合精度训练比 float16 略有改善；不过它使用的内存稍多一些。

总而言之，float16 和 bfloat16 混合精度训练在这里的表现相对相似，这并不意外。

而且有趣的是，bfloat16 更大的动态范围也让我们能够在不使用混合精度训练的情况下训练模型，而常规 float16 训练在这种情况下会失败。请注意，这里是一种幸运的巧合；根据我的经验，在许多情况下，纯 bfloat16 训练的效果并不如 bfloat16 混合精度训练。

## 高效的低精度推理与 LLaMA

混合精度训练可以扩展到深度学习模型的推理中，以提高效率、减少内存占用并加速计算。不过我们必须记住，在推理期间应用较低精度可能会因为数值精度降低而导致模型准确率轻微下降。然而，在许多深度学习应用中，对准确率的影响微乎其微，是为换取更少内存占用和更快计算而可以接受的折衷。

事实上，上面的混合精度微调代码在计算训练、验证和测试集准确率时，已经通过 Fabric 设置使用了 16 位精度进行推理。由于 DistilBERT 是一个相对较小的模型，推理速度只占总运行时间的很小一部分。

所以，为了加入一个稍微更有意思的推理示例，让我们看看 [Meta 的热门 LLaMA](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/)模型，用它来生成文本。这里，我们将使用用户友好的 [Lit-LLaMA 仓库](https://github.com/Lightning-AI/lit-llama)，它使用与我们前面相同的 Fabric 代码来实现 16 位精度。

不过，由于在数 TB 的数据上[预训练](https://sebastianraschka.com/glossary/#pretraining "Pretraining")一个大语言模型相当昂贵，我们将使用 Meta 现有的模型检查点在推理期间评估模型，生成新文本。

![Llm mixed precision copy llama screenshot](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/llama-screenshot.webp)

如果你是第一次使用这个仓库，请参阅 [Setup](https://github.com/Lightning-AI/lit-llama/blob/main/howto/download_weights.md) 一节来安装依赖，以及[下载权重的操作指南](https://github.com/Lightning-AI/lit-llama/blob/main/howto/download_weights.md)。

仓库设置好之后，我们可以使用 `generate.py` 脚本根据提示（prompt）生成文本，它默认使用 bfloat16：

```python
python generate.py --prompt "Large language models are" # uses bfloat16
Loading model ...
Time to load model: 24.84 seconds.
Global seed set to 1234
Large language models are an effective solution to the sequential inference task of natural language understanding, but are unfeasible for mobile applications. In this paper, we investigate a simple, yet effective approach to reduce the computational and memory demands of large language models by removing
Time for inference 1: 2.99 sec total, 16.70 tokens/sec
Memory used: 13.52 GB
```

为了与 float32 精度进行比较，我们必须手动修改脚本，把 Fabric 设备类型从 `torch.bfloat16` 改为 `torch.float32`。

![Llm mixed precision copy change llama](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/change-llama.webp)

修改之后，让我们用与上面相同的提示重新运行 [`generate.py`](http://generate.py/) 脚本：

```python
python generate.py \\
--prompt "Large language models are" # disabled bfloat16, using float32
Loading model ...
Time to load model: 17.93 seconds.
Global seed set to 1234
Large language models are an effective solution to the sequential 
data modelling tasks, but the huge size of these models makes them 
difficult to learn due to the large amount of parameters and the 
time to train them. The high computational cost, as well as the 
long training times
Time for inference 1: 4.36 sec total, 11.47 tokens/sec
Memory used: 27.02 GB
```

我们可以看到，模型现在使用的内存是原来的两倍，而且速度慢了 30%。

![Llm mixed precision copy llama speed 1](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/llama-speed-1.webp)

## 量化

如果我们想在推理期间进一步提高模型性能，我们还可以超越较低的浮点精度，使用量化。量化把模型权重从浮点数转换为低位宽的整数表示，例如 8 位整数（最近甚至有 4 位整数）。

不过，由于这篇博客文章已经很长了，我们将把更详细的解释留到以后的文章中。

与此同时，int8 量化（[LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale](https://arxiv.org/abs/2208.07339)）和 int4 量化（[GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](https://arxiv.org/abs/2210.17323)）都已经在 [Lit-LLaMA](https://github.com/Lightning-AI/lit-llama) 中得到支持，如果你想尝试的话！

## 结论

在本文中，我们看到了如何利用 16 位精度技术将一个 LLM 分类器的训练速度显著提升 3 倍。此外，我们还能把内存消耗减半！

此外，我们考察了生成式 AI 模型的推理速度，同样能够把性能提升 30%，同时让内存效率翻倍。

所以，如果你使用的 GPU 支持混合精度训练，值得加以利用，因为它简单到只需改变一行代码！

**致谢**

我要感谢 Luca Antiga 和 Adrian Waelchli 为提升本文清晰度提供的建设性反馈。
