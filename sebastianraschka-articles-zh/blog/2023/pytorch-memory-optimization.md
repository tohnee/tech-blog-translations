---
title: "PyTorch 大语言模型显存优化"
title_en: "PyTorch LLM Memory Optimization"
source: https://sebastianraschka.com/blog/2023/pytorch-memory-optimization.html
crawled: 2026-09-06
translated: 2026-09-06
---

# PyTorch 大语言模型显存优化

> 原文：[PyTorch LLM Memory Optimization](https://sebastianraschka.com/blog/2023/pytorch-memory-optimization.html)

峰值显存占用是训练视觉 Transformer 和大语言模型等深度学习模型时的常见瓶颈。本文提供了一系列可以把显存消耗降低约 20 倍的技术，同时不牺牲建模性能和预测准确率。

## 引言

在本文中，我们将探索 9 种易于上手的 PyTorch 显存优化技术。这些技术是可叠加的，也就是说我们可以在彼此的基础上继续应用。

我们将从 PyTorch 的 [Torchvision](https://pytorch.org/vision/stable/index.html) 库中的一个视觉 Transformer 入手，提供简单的代码示例，你可以在自己的机器上直接执行，而无需下载安装太多代码和数据集依赖。这个自包含的基线训练脚本约 100 行代码（不含空行和代码注释）。所有代码示例都可以在 [GitHub 上的这里](https://github.com/rasbt/pytorch-memory-optim)获取。

下面是我们要讲的章节与技术的提纲：

1. 微调一个视觉 Transformer
2. 自动混合精度训练
3. 低精度训练
4. 减小批次大小进行训练
5. 梯度累积与微批次
6. 选择更精简的优化器
7. 在目标设备上实例化模型
8. 分布式训练与张量分片
9. 参数卸载
10. 集大成：训练一个大语言模型

虽然本文以视觉 Transformer（即论文 [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929) 中的 ViT-L-16 模型）为例，但本文用到的所有技术同样适用于其他模型：卷积网络、大语言模型（LLM）等等。

此外，在用上述视觉 Transformer 示例逐个介绍完这些技术之后，我们会把它们应用到一个文本分类任务上，训练一个 BigBird-Roberta 大语言模型。如果没有这些技术，在消费级硬件上训练这样的模型是不可能的。

附言：注意本文有较多小节。为了不让文章进一步膨胀，我会刻意把每一节写得很短，但会提供指向各个主题更详细文章的链接。

## 1) 微调一个视觉 Transformer

为了简化实验用的 PyTorch 代码，我们将引入[开源的 Fabric 库](https://lightning.ai/docs/fabric/stable/)，它让我们只需几行（而非几十行）代码就能应用各种高级 PyTorch 技术（自动混合精度训练、多 GPU 训练、张量分片等）。

简单 PyTorch 代码与改用 Fabric 后的代码之间的差异很细微，只涉及少量修改，如下面的代码所示：

![Pytorch memory optimization 4 pytorch plus fabric](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/4_pytorch_plus_fabric.webp)

如上所述，这几处小改动为我们打开了使用 PyTorch 高级特性的大门（稍后就会看到），而且无需对现有代码做更多的结构调整。

概括上图，把纯 PyTorch 代码转换为 PyTorch+Fabric 主要有 3 个步骤：

![Pytorch memory optimization 5 steps](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/5_steps.webp)

1. 导入 Fabric 并实例化一个 Fabric 对象。
2. 使用 Fabric 来设置模型、优化器和数据加载器。
3. 对损失调用 `fabric.backward()`，而不是通常的 `loss.backward()`

这个视觉 Transformer 基于[原始 ViT 架构](https://arxiv.org/abs/2010.11929)，代码在这里可供查看。注意，我们是对模型做分类任务的微调，而不是从头训练来优化预测性能。

作为一个快速的合理性检查，纯 PyTorch 与带 Fabric 的 PyTorch 在预测性能和显存消耗上完全一致（+/- 由随机性带来的正常波动）：

**纯 PyTorch（[01\_pytorch-vit.py](https://github.com/rasbt/pytorch-memory-optim)）：**

```python
Time elapsed 17.94 min
Memory used: 26.79 GB
Test accuracy 95.85%
```

**带 Fabric 的 PyTorch（[01-2\_pytorch-fabric.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/01-2_pytorch-fabric.py)）**

```python
Time elapsed 17.88 min
Memory used: 26.84 GB
Test accuracy 96.06%
```

作为一个可选练习，欢迎你用这些代码做实验，把

```python
model = vit_l_16(weights=ViT_L_16_Weights.IMAGENET1K_V1)
```

替换为

```python
model = vit_l_16(weights=None)
```

这将从头训练同一个视觉 Transformer 架构，而不是微调它。如果你做了这个练习，会看到预测准确率从 >96% 跌到约 60%：

![Pytorch memory optimization 02 finetuning](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/02_finetuning.webp)

## 2) 自动混合精度

在上一节中，我们用 Fabric 修改了 PyTorch 代码。为什么要费这个周折？正如我们下面将看到的，现在只需改一行代码，就可以尝试混合精度和分布式训练等高级技术。

我们从混合精度训练开始，它已成为近年来训练深度神经网络的常规做法。

**应用混合精度训练**

只需一个很小的改动就能启用混合精度训练，把

```python
fabric = Fabric(accelerator="cuda", devices=1)
```

改成：

```python
fabric = Fabric(accelerator="cuda", devices=1, precision="16-mixed")
```

结果，我们的显存消耗从 26.84 GB 降到了 18.21 GB，而且不牺牲预测准确率，如下图所示。

![Pytorch memory optimization plot1 mixed](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/plot1-mixed.webp)

图题：对比 [01-2\_pytorch-fabric.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/01-2_pytorch-fabric.py) 与 [02\_mixed-precision.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/02_mixed-precision.py)

作为额外的好处，混合精度训练不仅降低了显存占用，还把运行时间缩短为原来的 1/6（从 17.88 分钟降到 3.45 分钟），这是个不错的附加收益；不过本文的重点仍是显存消耗，以免话题过于发散。

**什么是混合精度训练？**

[混合精度](https://sebastianraschka.com/glossary/#mixed-precision "Mixed Precision")训练同时使用 16 位和 32 位精度，以确保精度没有损失。以 16 位表示计算梯度要比 32 位格式快得多，并能节省大量显存。这一策略非常有用，尤其是在显存或算力受限的场景下。

它之所以叫"混合（mixed）"精度而不是"低（low）"精度训练，是因为我们并不会把*所有*参数和运算都转成 16 位浮点数。相反，我们在训练过程中在 32 位和 16 位运算之间切换，因此称为"混合"精度。

如下图所示，混合精度训练包括：把权重转换为较低精度（FP16）以加快计算、计算梯度、再把梯度转换回较高精度（FP32）以保证数值稳定性，最后用缩放后的梯度更新原始权重。

这种方式既能实现高效训练，又能保持神经网络的精度和稳定性。

![Pytorch memory optimization 8 mixed training](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/8_mixed-training.webp)

更多细节，我推荐阅读我更详细的独立文章 [Accelerating Large Language Models with Mixed-Precision Techniques](https://sebastianraschka.com/blog/2023/llm-mixed-precision-copy.html)，其中我对底层概念做了更深入的剖析。

## 3) 低精度训练

我们还可以更进一步，尝试以"完全"的低 16 位精度运行（而不是把中间结果转换为 32 位表示的混合精度）。

我们可以把

```python
fabric = Fabric(accelerator="cuda", precision="16-mixed")
```

改成以下内容来启用低精度训练：

```python
fabric = Fabric(accelerator="cuda", precision="16-true")
```

不过，你可能会注意到，运行这段代码时损失中会出现 NaN 值：

```python
Epoch: 0001/0001 | Batch 0000/0703 | Loss: 2.4105
Epoch: 0001/0001 | Batch 0300/0703 | Loss: nan
Epoch: 0001/0001 | Batch 0600/0703 | Loss: nan
...
```

这是因为常规的 16 位浮点数只能表示 -65,504 到 65,504 之间的数值：

```python
In [1]: import torch

In [2]: torch.finfo(torch.float16)
Out[2]: finfo(resolution=0.001, min=-65504, max=65504, eps=0.000976562, smallest_normal=6.10352e-05, tiny=6.10352e-05, dtype=float16)
```

所以，为了避免 NaN 问题，我们可以使用 "`bf16-true`" 设置。

```python
fabric = Fabric(accelerator="cuda", precision="bf16-true")
```

结果，我们可以把显存消耗进一步降到 13.82 GB（同样不牺牲准确率）：

![Pytorch memory optimization plot2 float16](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/plot2-float16.webp)

图题：[03\_bfloat16.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/03_bfloat16.py) 与前面几版代码的对比

**什么是 [Bfloat16](https://sebastianraschka.com/glossary/#bfloat16 "bfloat16")？**

`"bf16-mixed"` 中的 "bf16" 代表 [Brain Floating Point](https://cloud.google.com/tpu/docs/bfloat16)（bfloat16）。Google 为机器学习和深度学习应用开发了这种格式，尤其用于其 Tensor Processing Units（TPU）。与常规的 float16 格式相比，bfloat16 以牺牲精度为代价扩展了动态范围。

![Pytorch memory optimization bfloat16](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/bfloat16.webp)

扩展的动态范围让 bfloat16 能够表示非常大和非常小的数值，这使它更适合可能遇到大范围数值的深度学习应用。不过，较低的精度可能影响某些计算的准确性，或在某些情况下导致舍入误差。但在大多数深度学习应用中，这种精度损失对建模性能的影响微乎其微。

虽然 bfloat16 最初是为 TPU 开发的，但如今从属于 NVIDIA Ampere 架构的 A100 Tensor Core GPU 开始，多款 NVIDIA GPU 也支持这种格式。

你可以通过以下代码检查你的 GPU 是否支持 `bfloat16`：

```python
>>> import torch
>>> torch.cuda.is_bf16_supported()
True
```

## 4) 减小批次大小

我们来正面回应一个显而易见的问题：为什么不干脆减小批次大小？这通常确实是降低显存消耗的可行办法。不过，它有时会导致预测性能变差，因为这会改变训练动态。（更多细节，请参见[我的深度学习基础课程第 9.5 讲](https://lightning.ai/pages/courses/deep-learning-fundamentals/9.0-overview-techniques-for-speeding-up-model-training/unit-9.5-increasing-batch-sizes-to-increase-throughput/)。）

无论如何，让我们减小批次大小，看看它对结果的影响。结果表明，我们可以把批次大小降到 16，这会把显存消耗降到 5.69 GB，且不牺牲性能：

![Pytorch memory optimization plot23 batchsize](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/plot23-batchsize.webp)

图题：[04\_lower-batchsize.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/04_lower-batchsize.py) 与前面几版代码的对比。

## 5) 使用梯度累积构造微批次

梯度累积是一种在训练中"虚拟地"增大批次大小的方法，当可用的 GPU 显存不足以容纳期望的批次大小时非常有用。注意，这只影响运行时间，不影响建模性能。

在梯度累积中，先对较小的批次计算梯度，并在多次迭代中将其累积（通常是求和或求平均），而不是每个批次后都更新模型权重。一旦累积的梯度达到目标"虚拟"批次大小，就用累积的梯度更新模型权重。

要启用梯度累积，只需对前向和反向传播做两处小改动：

![Pytorch memory optimization gradient acc](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/gradient-acc.webp)

图题：[05\_gradient-accum.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/05_gradient-accum.py) 中的代码改动

我在文章 [Finetuning LLMs on a Single GPU Using Gradient Accumulation](https://sebastianraschka.com/blog/2023/llm-grad-accumulation.html) 中更详细地介绍过梯度累积。

使用 16 的有效批次大小和 4 个累积步骤，意味着我们实际使用的批次大小为 4（因为 16 / 4 = 4）。

![Pytorch memory optimization plot4 gradacc](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/plot4-gradacc.webp)

图题：[05\_gradient-accum.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/05_gradient-accum.py) 的结果

这项技术的一个缺点是运行时间从 3.96 分钟增加到了 12.91 分钟。

当然，我们甚至可以更小，用 16 个累积步骤。这会带来大小为 1 的微批次，把显存占用进一步降低（约 75%），但这个我就留作可选练习了。

## 6) 使用更精简的优化器

你知道吗，流行的 Adam 优化器带有额外的参数？举例来说，Adam 会为每个模型参数维护 2 个额外的优化器参数（一个均值和一个方差）。

因此，把 Adam 换成 SGD 这样的无状态优化器，我们可以把参数数量减少 2/3，这在处理视觉 Transformer 和大语言模型时相当可观。

纯 SGD 的缺点是收敛性质通常较差。所以，让我们把 Adam 换成 SGD，并引入余弦衰减学习率调度器来弥补这一点、获得更好的收敛。

简而言之，我们会把之前使用的 Adam 优化器：

```python
optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)
```

换成 SGD 优化器加调度器：

```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

num_steps = NUM_EPOCHS * len(train_loader)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=num_steps)
```

有了这一改动，我们得以降低峰值显存占用，同时保持约 97% 的分类准确率：

![Pytorch memory optimization plot5 sgd](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/plot5_sgd.webp)

图题：[06\_sgd-with-scheduler.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/06_sgd-with-scheduler.py) 的结果

如果你想了解更多，我在[深度学习基础课程的第 6.5 单元](https://lightning.ai/pages/courses/deep-learning-fundamentals/unit-6-overview-essential-deep-learning-tips-tricks/unit-6.2-learning-rates-and-learning-rate-schedulers/)中更详细地讨论了学习率调度器（包括 1-cycle 调度中的余弦衰减）。

## 7) 以目标精度在目标设备上创建模型

当我们在 PyTorch 中实例化一个模型时，通常先在 CPU 设备上创建它，然后再把它转移到目标设备并转换为所需的精度：

```python
model = vit_l_16(weights=ViT_L_16_Weights.IMAGENET1K_V1)
model.cuda().float16()
```

考虑到 CPU 上的中间模型表示是全精度的，这样做可能效率不高。作为替代，我们可以使用 Fabric 中的 `init_module` 上下文，直接在目标设备（如 GPU）上以所需精度创建模型：

```python
import lightning as L

fabric = Fabric(accelerator="cuda", devices=1, precision="16-true")

with fabric.init_module():
    model = vit_l_16(weights=ViT_L_16_Weights.IMAGENET1K_V1)
```

在这个具体案例（这个模型）中，前向传播期间的峰值显存会大于全精度表示下的模型大小。所以，我们将仅针对模型加载本身来[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark") `fabric.init_module` 方式。

- 不用 `init_module` 时的 GPU 显存峰值：1.24 GB（07\_01\_init-module.py）
- 使用 `init_module` 时的 GPU 显存峰值：0.65 GB（07\_03\_init-module.py）

从上面的结果可以看出，在这种情形下，`init_module` 把模型加载的峰值显存需求降低了 50%。我们将在本文后面用到这项技术。

关于 `init_module` 的更多细节，请参阅更详细的文章 [Efficient Initialization of Large Models](https://lightning.ai/pages/community/efficient-initialization-of-large-models/)。

## 8) 分布式训练与张量分片

我们要尝试的下一个改动是多 GPU 训练。如果我们手头有多块 GPU，它会很有用，因为它让我们能够更快地训练模型。

不过，这里我们主要关心的是节省显存。所以，我们将使用一种更高级的分布式多 GPU 策略，称为全分片数据并行（Fully Sharded Data Parallelism，FSDP），它同时利用数据并行和张量并行，把大型权重矩阵分片到多个设备上。

注意，这个模型本来就很小，因此在第 7 节代码的基础上添加这项技术不会看到什么明显效果。所以，为了聚焦于分片的纯粹效果，我们将把这份代码与第 1 节的全精度基线进行对比。

我们把

```python
fabric = Fabric(accelerator="cuda", devices=1)
```

改为

```python
auto_wrap_policy = partial(
    transformer_auto_wrap_policy,
    transformer_layer_cls={EncoderBlock})
    
strategy = FSDPStrategy(
    auto_wrap_policy=auto_wrap_policy,      
    activation_checkpointing=EncoderBlock)

fabric = Fabric(accelerator="cuda", devices=4, strategy=strategy)
```

![Pytorch memory optimization plot6 tensor sharding](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/plot6_tensor-sharding.webp)

图题：[08\_fsdp-with-01-2.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/08_fsdp-with-01-2.py) 的结果

注意，除了像上面那样手动定义策略之外，我们也可以直接使用下面这行，它会自动决定对哪些层做分片：

```python
fabric = Fabric(accelerator="cuda", devices=4, strategy="fsdp")
```

**理解数据并行与张量并行**

在数据并行中，小批次（mini-batch）被切分，每块 GPU 上都有一份模型副本。由于多块 GPU 并行工作，这一过程可以加速模型训练。

![Pytorch memory optimization 11 data parallelism](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/11_data-parallelism.webp)

简单来说，它的工作方式如下：

1. 同一个模型被复制到所有 GPU 上。
2. 然后每块 GPU 被喂入输入数据的不同子集（不同的小批次）。
3. 所有 GPU 独立执行模型的前向和反向传播，计算各自的局部梯度。
4. 然后，在所有 GPU 之间收集梯度并求平均。
5. 再用平均后的梯度更新模型参数。

这种方式的主要优势是速度。由于每块 GPU 都在与其他 GPU 并发地处理一个不同的小批次数据，模型可以在更少的时间内处理更多数据。这可以显著缩短训练模型所需的时间，尤其是在处理大型数据集时。

然而，数据并行也有一些局限。最重要的是，每块 GPU 都必须拥有模型及其参数的完整副本。这限制了我们能训练的模型规模，因为模型必须能装进单块 GPU 的显存——这对现代视觉 Transformer 或大语言模型来说并不可行。

与把小批次切分到多个设备上的数据并行不同，张量并行是把模型本身切分到多块 GPU 上。在数据并行中，每块 GPU 都要装下整个模型，这在训练较大模型时可能成为限制。而张量并行则通过把模型拆开、分布到多个设备上，使得训练那些对单块 GPU 来说过大的模型成为可能。

![Pytorch memory optimization 12 tensor parallelism](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/12_tensor-parallelism.webp)

它是如何工作的？想想矩阵乘法。分发它有两种方式——按行或按列。为简单起见，我们考虑按列分发。例如，我们可以把一次大矩阵乘法运算拆分成多个独立计算，每个都可以在不同的 GPU 上执行，如下图所示。然后再把结果拼接起来得到原始结果，从而有效地分摊计算负载。

![Pytorch memory optimization tensor parallelism](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/tensor-parallelism.webp)

## 9) 参数卸载

除了上一节讲解的 FSDP 策略之外，我们还可以把优化器参数卸载（offload）到 CPU 上，只需把

```python
strategy = FSDPStrategy(
    auto_wrap_policy=auto_wrap_policy,      
    activation_checkpointing=EncoderBlock,
)
```

改为

```python
strategy = FSDPStrategy(
    auto_wrap_policy=auto_wrap_policy,      
    activation_checkpointing=EncoderBlock,
    cpu_offload=True
)
```

这会把显存消耗从 6.59 GB 降到 6.03 GB：

![Pytorch memory optimization plot7 cpu offload](https://sebastianraschka.com/images/blog/2023/pytorch-memory-optimization/plot7_cpu-offload.webp)

图题：[09\_fsdp-cpu-offload-with-01-2.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/09_fsdp-cpu-offload-with-01-2.py) 的结果。

唯一的小缺点是运行时间从 5.5 分钟增加到了 8.3 分钟。

## 10) 集大成并训练一个大语言模型

在前面的章节中，我们围绕视觉 Transformer 涵盖了大量内容。当然，你们中可能有人也想知道这些技术是否适用于大语言模型。答案是：当然适用！

我们在 [Lit-LLaMA](https://github.com/Lightning-AI/lit-llama) 和 [Lit-GPT](https://github.com/Lightning-AI/lit-gpt) 仓库中使用了其中许多技巧，它们支持 LLaMA、Falcon、Pythia 以及其他热门模型。不过，为了构造一个更通用的例子，我们将微调来自流行的 HF [`transformers`](https://github.com/huggingface/transformers) 库的一个大语言模型，用于对 IMDb 电影评论做情感分类。

例如，如果使用上述技术，你只需 1.15 GB 显存（[bonus\_distilbert-after.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/bonus_distilbert-after.py)）就能训练一个 [DistilBERT](https://arxiv.org/abs/1910.01108) 分类器，而不是 3.99 GB（[bonus\_bigbird-before.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/bonus_bigbird-before.py)）。

更令人印象深刻的是，把这些技术应用到 transformers 库中的 [BigBird](https://arxiv.org/abs/2007.14062) 模型上，BigBird 只消耗 4.03 GB 显存（[bonus\_bigbird-after.py](https://github.com/rasbt/pytorch-memory-optim/blob/main/bonus_bigbird-after.py)）！

```python
  strategy = FSDPStrategy(
        cpu_offload=True
   )

   fabric = Fabric(
        accelerator="cuda",
        devices=4,
        strategy=strategy,
         precision="bf16-true"
   )

   with fabric.init_module():
       model = AutoModelForSequenceClassification.from_pretrained(
            "google/bigbird-roberta-base", num_labels=2)
```

（我本想把不使用这些技术时的性能数据也附上作为参考，但如果不做上述优化，这个模型根本无法运行。）

## 结论

本文展示了 9 种降低 PyTorch 模型显存消耗的技术。把这些技术应用到视觉 Transformer 上时，我们在单块 GPU 上把显存消耗降低了 20 倍。我们还看到，跨 GPU 的张量分片可以进一步降低显存消耗。同样的优化也让仅用 4 GB 的 GPU 显存峰值训练一个 BigBird 大语言模型成为可能。

这些技术没有一项是特定于某个模型的，几乎可以用于任何 PyTorch 训练脚本。而且借助开源的 Fabric 库，其中大多数优化只需一行代码即可启用。
