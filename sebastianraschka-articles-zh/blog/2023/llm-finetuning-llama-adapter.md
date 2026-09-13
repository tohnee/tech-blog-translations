---
title: "参数高效的 LLM 微调"
title_en: "Parameter-Efficient LLM Finetuning"
source: https://sebastianraschka.com/blog/2023/llm-finetuning-llama-adapter.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 参数高效的 LLM 微调

> 原文：[Parameter-Efficient LLM Finetuning](https://sebastianraschka.com/blog/2023/llm-finetuning-llama-adapter.html)

在快速演进的人工智能领域，以高效且有效的方式使用大语言模型正变得越来越重要。

[参数高效微调](https://sebastianraschka.com/glossary/#lora "LoRA (Low-Rank Adaptation)")正处在这一追求的前沿，它让研究人员和从业者能够在复用预训练模型的同时，把计算和资源开销降到最低。它还让我们能在更广泛的硬件上训练 AI 模型，包括计算能力有限的设备，例如笔记本电脑、智能手机和物联网设备。最后，随着人们对环境可持续性的关注日益增加，参数高效微调还降低了训练大规模 AI 模型带来的能耗和碳足迹。

总而言之，参数高效微调之所以有用，至少有以下 5 个原因：

1. 降低计算成本（需要更少的 GPU 和 GPU 时间）；
2. 更快的训练时间（更快完成训练）；
3. 更低的硬件要求（可以在更小的 GPU 和更少的内存上运行）；
4. 更好的建模性能（减少过拟合）；
5. 更少的存储空间（大部分权重可以在不同任务之间共享）。

本文解释微调的总体概念，并讨论流行的参数高效替代方案，例如前缀调优（prefix tuning）和适配器（adapter）。最后，我们将介绍近期的 LLaMA-Adapter 方法，看看如何在实践中使用它。

## 微调大语言模型

自 GPT-2（[Radford et al.](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)）和 GPT-3（[Brown et al.](https://arxiv.org/abs/2005.14165)）以来，我们已经看到，在通用文本语料库上预训练的生成式大语言模型（LLM）具备[上下文学习](https://sebastianraschka.com/glossary/#few-shot-prompting "Few-Shot Prompting")能力——如果我们要执行 LLM 未被显式训练过的特定任务或新任务，并不需要进一步训练或微调预训练 LLM。相反，我们可以直接在输入提示中提供目标任务的少量示例，如下例所示。

![Llm finetuning llama adapter in context](https://sebastianraschka.com/images/blog/2023/llm-finetuning-llama-adapter/in-context.webp)

对于无法直接访问大语言模型（LLM）的场景，例如通过 API 或用户界面与 LLM 交互时，上下文学习是一种宝贵且对用户友好的方法。

然而，如果我们能够访问 LLM，使用来自目标领域的数据在目标任务上对其进行适配和微调，通常会带来更好的结果。那么，我们如何把模型适配到目标任务？下图概述了三种传统方法。

![Llm finetuning llama adapter classic flowchart](https://sebastianraschka.com/images/blog/2023/llm-finetuning-llama-adapter/classic-flowchart.webp)

### 基于特征的方法

在基于特征的方法中，我们加载一个预训练 LLM 并将其应用到目标数据集上。这里我们特别关注为训练集生成输出嵌入，然后可以把这些嵌入用作训练分类模型的输入特征。虽然这种方法在以嵌入为核心的模型（如 BERT）中特别常见，我们同样可以从生成式 GPT 风格的模型中提取嵌入（你可以在我的博客文章[*Finetuning Large Language Models On A Single GPU Using Gradient Accumulation*](https://sebastianraschka.com/blog/2023/llm-grad-accumulation.html)中找到一个例子）。

这个分类模型可以是逻辑回归模型、随机森林或 XGBoost——一切随你所愿。（不过，根据我的经验，逻辑回归这类线性分类器在这里表现最好。）

从概念上讲，我们可以用下面的代码来说明基于特征的方法：

```python
model = AutoModel.from_pretrained("distilbert-base-uncased")

# ...
# tokenize dataset
# ...

# generate embeddings
@torch.inference_mode()
def get_output_embeddings(batch): 
    output = model(
        batch["input_ids"],
        attention_mask=batch["attention_mask"]
    ).last_hidden_state[:, 0]
return {"features": output}
  
dataset_features = dataset_tokenized.map(
  get_output_embeddings, batched=True, batch_size=10)

X_train = np.array(dataset_features["train"]["features"])
y_train = np.array(dataset_features["train"]["label"])

X_val = np.array(dataset_features["validation"]["features"])
y_val = np.array(dataset_features["validation"]["label"])

X_test = np.array(dataset_features["test"]["features"])
y_test = np.array(dataset_features["test"]["label"])

# train classifier
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression()
clf.fit(X_train, y_train)

print("Training accuracy", clf.score(X_train, y_train))
print("Validation accuracy", clf.score(X_val, y_val))
print("test accuracy", clf.score(X_test, y_test))
```

（感兴趣的读者可以在[这里](https://github.com/rasbt/blog-finetuning-llama-adapters/blob/main/three-conventional-methods/1_distilbert-feature-extractor.ipynb)找到完整代码示例。）

### 微调 I——更新输出层

与上述基于特征的方法相关的一种流行做法是微调输出层（我们把这种方法称为*微调 I*）。与基于特征的方法类似，我们保持预训练 LLM 的参数冻结，只训练新添加的输出层，类似于在嵌入特征上训练逻辑回归分类器或小型多层感知机。

用代码表示大致如下：

```python
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
     num_labels=2  # suppose target task is a binary classification task
) 

# freeze all layers
for param in model.parameters():
    param.requires_grad = False
    
# then unfreeze the two last layers (output layers)
for param in model.pre_classifier.parameters():
    param.requires_grad = True

for param in model.classifier.parameters():
    param.requires_grad = True
    
# finetune model
lightning_model = CustomLightningModule(model)

trainer = L.Trainer(
    max_epochs=3,
    ...
)

trainer.fit(
  model=lightning_model,
  train_dataloaders=train_loader,
  val_dataloaders=val_loader)

# evaluate model
trainer.test(lightning_model, dataloaders=test_loader)
```

（感兴趣的读者可以在[这里](https://github.com/rasbt/blog-finetuning-llama-adapters/blob/main/three-conventional-methods/2_finetune-last-layers.ipynb)找到完整代码示例。）

理论上，由于我们使用的是同一个冻结的骨干模型，这种方法在建模性能和速度上应与基于特征的方法相近。不过，由于基于特征的方法让"预计算并存储训练数据集的嵌入特征"稍微更容易一些，它在某些特定实际场景中可能更方便。

### 微调 II——更新所有层

虽然最初的 BERT 论文（[Devlin et al.](https://arxiv.org/abs/1810.04805)）报告说只微调输出层就能取得与微调所有层相当的建模性能——后者由于涉及更多参数而代价高得多。例如，一个 BERT [基础模型](https://sebastianraschka.com/glossary/#base-model "Base Model")大约有 1.1 亿个参数，而用于二分类的 BERT 基础模型的最后一层只有区区 1,500 个参数。此外，BERT 基础模型的最后两层合计占 60,000 个参数——仅约为模型总规模的 0.6%。

最终效果会因我们的目标任务和目标领域与模型预训练数据集的相似程度而有所不同。但在实践中，微调所有层几乎总能带来更好的建模性能。

因此，在优化建模性能时，使用预训练 LLM 的黄金标准是更新所有层（这里称为微调 II）。概念上微调 II 与微调 I 非常相似，唯一的区别是我们不冻结预训练 LLM 的参数，而是连它们一起微调：

```python
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
     num_labels=2  # suppose target task is a binary classification task
) 

# don't freeze layers
# for param in model.parameters():
#    param.requires_grad = False
    

# finetune model
lightning_model = LightningModel(model)

trainer = L.Trainer(
    max_epochs=3,
    ...
)

trainer.fit(
  model=lightning_model,
  train_dataloaders=train_loader,
  val_dataloaders=val_loader)

# evaluate model
trainer.test(lightning_model, dataloaders=test_loader)
```

（感兴趣的读者可以在[这里](https://github.com/rasbt/blog-finetuning-llama-adapters/blob/main/three-conventional-methods/2_finetune-last-layers.ipynb)找到完整代码示例。）

如果你想知道一些真实世界的结果：上面的代码片段被用来训练一个影评分类器，使用的是预训练的 DistilBERT 基础模型（代码 notebook 可以在[这里](https://github.com/rasbt/blog-finetuning-llama-adapters/tree/main/three-conventional-methods)获取）：

- 基于特征的方法 + 逻辑回归：83% 测试准确率
- 微调 I，更新最后 2 层：87% 准确率
- 微调 II，更新所有层：92% 准确率。

这些结果与一条普遍的经验法则一致：微调更多层往往带来更好的性能，但代价也更高。

![Llm finetuning llama adapter classic performance](https://sebastianraschka.com/images/blog/2023/llm-finetuning-llama-adapter/classic-performance.webp)

## 参数高效微调

在前面的章节中，我们了解到微调更多层通常会带来更好的结果。不过，上面的实验是基于相对较小的 DistilBERT 模型的。如果我们想微调那些勉强塞得进 GPU 显存的大模型——例如最新的生成式 LLM——该怎么办？当然，我们可以使用上面的基于特征的方法或微调 I。但假如我们想获得与微调 II 相当的建模质量呢？

多年来，研究人员开发了多种技术（[Lialin et al.](https://arxiv.org/abs/2303.15647)），可以只训练少量参数就高质量地微调 LLM。这些方法通常被称为参数高效微调技术（PEFT）。

一些使用最广泛的 PEFT 技术总结在下图中。

![Llm finetuning llama adapter popular methods](https://sebastianraschka.com/images/blog/2023/llm-finetuning-llama-adapter/popular-methods.webp)

最近引起巨大反响的一种 PEFT 技术是 LLaMA-Adapter，它是为 Meta 广受欢迎的 LLaMA 模型提出的（[Touvron et al.](https://arxiv.org/abs/2302.13971)）——不过，虽然 LLaMA-Adapter 是在 LLaMA 的背景下提出的，这个想法本身是与具体模型无关的。

要理解 LLaMA-Adapter 的工作原理，我们需要（小小地）退一步，回顾两种相关技术：*前缀调优*（prefix tuning）和*适配器*（adapter）——LLaMA-Adapter（[Zhang et al.](https://arxiv.org/abs/2303.16199)）结合并扩展了这两种想法。

因此，在本文余下部分，我们将讨论提示修改的各种概念，以理解前缀调优和适配器方法，然后再仔细研究 LLaMA-Adapter。（低秩适配（low-rank adaptation）我们留到以后的文章再讲。）

## 提示调优与前缀调优

提示调优（prompt tuning）的原始概念指的是通过改变输入提示来获得更好建模结果的技术。例如，假设我们想把一句英文翻译成德文。我们可以用多种不同的方式向模型提问，如下图所示。

![Llm finetuning llama adapter hard prompting](https://sebastianraschka.com/images/blog/2023/llm-finetuning-llama-adapter/hard-prompting.webp)

上面展示的这个概念被称为*硬*（hard）提示调优，因为我们直接改变的是离散的输入 token，它们是不可微的。

与*硬*提示调优相对，*软*（soft）提示调优则把输入 token 的嵌入与一个可训练张量拼接起来，这个张量可以通过反向传播进行优化，以提升在目标任务上的建模性能。

提示调优的一个具体变体是前缀调优（[Li and Liang](https://arxiv.org/abs/2101.00190)）。前缀调优的想法是向每个 transformer 块添加一个可训练张量，而不像*软*提示调优那样只作用于[输入嵌入](https://sebastianraschka.com/glossary/#token-embeddings "Token Embeddings")。下图展示了常规 transformer 块与经前缀修改的 transformer 块之间的区别。

![Llm finetuning llama adapter prefix tuning](https://sebastianraschka.com/images/blog/2023/llm-finetuning-llama-adapter/prefix-tuning.webp)

请注意，上图中的"全连接层"指的是一个小型多层感知机（两个全连接层，中间夹一个非线性激活函数）。这些全连接层把软提示嵌入到一个与 transformer 块输入维度相同的特征空间中，以保证拼接时的兼容性。

用（Python）伪代码，我们可以如下展示常规 transformer 块与经前缀修改的 transformer 块之间的区别：

![Llm finetuning llama adapter prefix code](https://sebastianraschka.com/images/blog/2023/llm-finetuning-llama-adapter/prefix-code.webp)

根据最初的前缀调优[论文](https://arxiv.org/abs/2101.00190)，前缀调优只需训练 0.1% 的参数即可达到与微调所有层相当的建模性能——实验基于 GPT-2 模型。此外，在许多情况下，前缀调优甚至超过了微调所有层的表现，这很可能是因为涉及的参数更少，有助于在较小的目标数据集上减少过拟合。

最后，澄清一下软提示在推理时的使用方式：学习到一个软提示后，在执行我们微调模型所针对的特定任务时，必须把它作为前缀提供。这使模型能够把它的输出适配到那个特定任务。此外，我们可以拥有多个软提示，每个对应一个不同的任务，并在推理时提供相应的前缀，以在特定任务上取得最优结果。

## 适配器

最初的*适配器*方法（[Houlsby et al.](https://arxiv.org/abs/1902.00751)）与前面提到的*前缀调优*有一定关联，因为它们同样向每个 transformer 块添加额外的参数。不过，适配器方法不是在输入嵌入前拼接前缀，而是在两个位置添加适配器层，如下图所示。

![Llm finetuning llama adapter adapter outline](https://sebastianraschka.com/images/blog/2023/llm-finetuning-llama-adapter/adapter-outline.webp)

对于偏好（Python）伪代码的读者，适配器层可以写成如下形式：

![Llm finetuning llama adapter adapter](https://sebastianraschka.com/images/blog/2023/llm-finetuning-llama-adapter/adapter.webp)

请注意，适配器的全连接层通常相对较小，并且具有类似于自编码器的瓶颈结构。每个适配器块的第一个全连接层把输入降维到低维表示，第二个全连接层再把输入投影回输入维度。这为什么是参数高效的？例如，假设第一个全连接层把 1024 维输入投影到 24 维，第二个全连接层再投影回 1024 维。这意味着我们引入了 1,024 x 24 + 24 x 1,024 = 49,152 个权重参数。相比之下，一个把 1024 维输入重新投影到 1,024 维空间的单一全连接层将拥有 1,024 x 1024 = 1,048,576 个参数。

根据最初的[适配器论文](https://arxiv.org/abs/1902.00751)，使用适配器方法训练的 BERT 模型只需训练 3.6% 的参数，就能达到与完全微调的 BERT 模型相当的建模性能。

那么，问题来了：适配器方法与前缀调优相比如何？根据最初的前缀调优[论文](https://arxiv.org/abs/2101.00190)，当只调优模型总参数的 0.1% 时，适配器方法的表现略逊于前缀调优方法。然而，当适配器方法用于调优模型参数的 3% 时，该方法与前缀调优 0.1% 的成绩持平。因此，我们可以得出结论：前缀调优是两者中更高效的方法。

## 扩展前缀调优与适配器：LLaMA-Adapter

在前缀调优和原始适配器方法想法的基础上，研究人员最近提出了 LLaMA-Adapter（[Zhang et al.](https://arxiv.org/abs/2303.16199)），一种针对 [LLaMA](https://github.com/facebookresearch/llama) 的参数高效微调方法（LLaMA 是 Meta 推出的流行的 GPT 替代品）。

与*前缀调优*一样，LLaMA-Adapter 方法在嵌入输入之前拼接（prepend）可调的提示张量。值得注意的是，在 LLaMA-Adapter 方法中，前缀是在一个嵌入表内学习和维护的，而不是外部提供的。模型中的每个 transformer 块都有自己独特的已学习前缀，从而在不同模型层之间实现更有针对性的适配。

此外，LLaMA-Adapter 引入了零初始化注意力机制并结合门控。这种所谓 *zero-init* 注意力与门控背后的动机是：适配器和前缀调优可能会通过引入随机初始化的张量（前缀提示或适配器层）而破坏预训练 LLM 的语言知识，导致微调不稳定以及初始训练阶段的高损失值。

与前缀调优和原始适配器方法相比的另一个差异是：LLaMA-Adapter 只把可学习的适配提示添加到最顶层的 *L* 个 transformer 层，而不是所有 transformer 层。作者认为这种做法能够更有效地调优专注于更高层级语义信息的语言表示。

虽然 LLaMA 适配器方法的基本思想与前缀调优相关（拼接可调的软提示），但在具体实现方式上还存在一些额外的细微差别。例如，只有[自注意力](https://sebastianraschka.com/glossary/#mha "Multi-Head Attention (MHA)")输入的键（key）和值（value）序列会通过可调软提示进行修改。然后，根据门控因子（训练开始时被设为零），经前缀修改的注意力要么被采用，要么不被采用。下面的可视化展示了这一概念。

![Llm finetuning llama adapter llama adapter](https://sebastianraschka.com/images/blog/2023/llm-finetuning-llama-adapter/llama-adapter.webp)

用伪代码可以这样表达：

![Llm finetuning llama adapter llama adapter code](https://sebastianraschka.com/images/blog/2023/llm-finetuning-llama-adapter/llama-adapter-code.webp)

简而言之，LLaMA-Adapter 与常规前缀调优的区别在于：LLaMA-Adapter 只修改顶部的（即前面几层）transformer 块，并引入门控机制来稳定训练。虽然研究人员专门在 LLaMA 上进行了实验，他们提出的 Adapter 方法是一种通用方法，也可以应用于其他类型的 LLM（例如 GPT）。

使用 LLaMA-Adapter 方法，研究人员仅用 1 小时（使用 8 块 A100 GPU）就在一个包含 52k 指令对的数据集上微调了一个 70 亿参数的 LLaMA 模型。此外，微调后的 LLaMA-Adapter 模型在该研究比较的所有模型中，在问答任务上表现最佳，而只需微调 1.2 M 个参数（适配器层）。

如果你想了解 LLaMA-Adapter 方法，可以在[这里](https://github.com/ZrrSkywalker/LLaMA-Adapter)找到基于 GPL 许可 LLaMA 代码的原始实现。

另外，如果你的使用场景与 GPL 许可证不兼容（该许可证要求你以类似许可开源所有衍生作品），请查看 [Lit-LLaMA GitHub 仓库](https://github.com/Lightning-AI/lit-llama)。Lit-LLaMA 是基于 Apache 许可的 nanoGPT 代码实现的 LLaMA 可读实现，其许可条款限制更少。

具体来说，如果你有兴趣使用 LLaMA-Adapter 方法微调 LLaMA 模型，可以运行来自 [Lit-LLaMA GitHub 仓库](https://github.com/Lightning-AI/lit-llama)的

```python
python finetune_adapter.py
```

脚本。

## 结论

微调预训练大语言模型（LLM）是让这些模型适配特定业务需求、对齐目标领域数据的有效方法。这一过程通过使用与目标领域相关的较小数据集调整模型参数，使模型学习领域特定的知识和词汇。

然而，由于 LLM 是"大"模型，更新 transformer 模型中的多层可能非常昂贵，于是研究人员开始开发参数高效的替代方案。

在本文中，我们讨论了几种替代传统 LLM 微调机制的参数高效方案。具体而言，我们介绍了通过前缀调优拼接可调软提示，以及插入额外的适配器层。

最后，我们讨论了近期流行的 LLaMA-Adapter 方法，它在拼接可调软提示的同时引入了额外的门控机制来稳定训练。

如果你想在实践中尝试这些方法，请查看 [Lit-LLaMA 仓库](https://github.com/Lightning-AI/lit-llama)——欢迎提出问题，也欢迎推荐更多参数高效微调方法！

**致谢**

我要感谢 Carlos Mocholi、Luca Antiga 和 Adrian Waelchli，感谢他们为提升本文清晰度提供的建设性反馈。
