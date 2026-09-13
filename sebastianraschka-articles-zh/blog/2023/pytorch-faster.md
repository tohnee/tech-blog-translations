---
title: "PyTorch 训练提速技巧"
title_en: "PyTorch Training Speed Techniques"
source: https://sebastianraschka.com/blog/2023/pytorch-faster.html
crawled: 2026-09-06
translated: 2026-09-06
---

# PyTorch 训练提速技巧

> 原文：[PyTorch Training Speed Techniques](https://sebastianraschka.com/blog/2023/pytorch-faster.html)

这篇博文介绍一些在不损害模型精度的前提下提升 PyTorch 模型训练性能的技巧。为此，我们会把 PyTorch 模型包装进 LightningModule，并使用 Trainer 类来启用各种训练优化。只需改动几行代码，我们就能把单 GPU 上的训练时间从 22.53 分钟缩短到 2.75 分钟，同时保持模型的预测精度。

没错，这就是 8 倍的性能提升！

![(本文已于 2023 年 3 月 17 日更新，现在使用 PyTorch 2.0 和 Lightning 2.0！)](https://sebastianraschka.com/images/blog/2023/pytorch-faster/benchmark-last.webp)

**（本文已于 2023 年 3 月 17 日更新，现在使用 PyTorch 2.0 和 Lightning 2.0！）**

## 引言

在本教程中，我们将微调一个 [DistilBERT 模型](https://arxiv.org/abs/1910.01108)——BERT 的蒸馏版本，体积缩小了 40%，而预测性能几乎不变。
微调预训练语言模型有几种不同的做法。下图描绘了其中三种最常见的方式。

![Pytorch 提速：三种技术](https://sebastianraschka.com/images/blog/2023/pytorch-faster/3-techniques.webp)

上面三种做法（a-c）都假设我们已经用自监督学习在无标签数据集上对模型做了预训练。随后在第 2 步把模型迁移到目标任务时，我们可以：

- a) 提取嵌入（embedding），并在其上训练一个分类器（例如可以是 scikit-learn 的支持向量机）；
- b) 替换/添加输出层，微调 transformer 的最后一层（或最后几层）；
- c) 替换/添加输出层，微调所有层。

做法 a-c 按计算效率从高到低排列，其中 a) 通常最快。根据我的经验，这个排序也反映了模型的预测性能：c) 通常能取得最高的预测准确率。

本教程中，我们将采用做法 c)，训练一个模型来预测 [IMDB Large Movie Review](https://ai.stanford.edu/~amaas/data/sentiment/) 数据集中影评的情感倾向，该数据集共包含 50,000 条影评。

## 1) 纯 PyTorch 基线

作为热身练习，我们先从纯 PyTorch 基线开始：在 IMDB 影评数据集上训练 DistilBERT 模型。如果你想亲自运行代码，可以按如下方式搭建一个装有相关 Python 库的虚拟环境：

```python
conda create -n faster-blog python=3.9
conda activate faster-blog

pip install watermark transformers datasets torchmetrics lightning
```

供参考，我所使用的相关软件版本如下（运行本文后面的代码时，它们会被打印到终端上）：

```python
Python version: 3.9.15
torch         : 2.0.0+cu118
lightning     : 2.0.0
transformers  : 4.26.1
```

为了避免让本文被枯燥的数据加载工具代码撑爆，我会略过 [local\_dataset\_utilities.py](https://github.com/rasbt/faster-pytorch-blog/blob/main/local_dataset_utilities.py) 文件，其中包含加载数据集的代码。这里唯一需要知道的信息是：我们把数据集划分为 35,000 个训练样本、5,000 条验证集记录和 10,000 条测试记录。

下面来看主要的 PyTorch 代码。这段代码是自成一体的，只有数据加载工具放在了 [local\_dataset\_utilities.py](https://github.com/rasbt/faster-pytorch-blog/blob/main/local_dataset_utilities.py) 文件中。请先浏览一遍这段 PyTorch 代码，稍后我们再讨论：

```python
import os
import os.path as op
import time

from datasets import load_dataset
import torch
from torch.utils.data import DataLoader
import torchmetrics
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from watermark import watermark

from local_dataset_utilities import (
    download_dataset,
    load_dataset_into_to_dataframe,
    partition_dataset,
)
from local_dataset_utilities import IMDBDataset

def tokenize_text(batch):
    return tokenizer(batch["text"], truncation=True, padding=True)

def train(num_epochs, model, optimizer, train_loader, val_loader, device):
    for epoch in range(num_epochs):
        train_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2).to(device)

        for batch_idx, batch in enumerate(train_loader):
            model.train()
            for s in ["input_ids", "attention_mask", "label"]:
                batch[s] = batch[s].to(device)

            ### FORWARD AND BACK PROP
            outputs = model(
                batch["input_ids"],
                attention_mask=batch["attention_mask"],
                labels=batch["label"],
            )
            optimizer.zero_grad()
            outputs["loss"].backward()

            ### UPDATE MODEL PARAMETERS
            optimizer.step()

            ### LOGGING
            if not batch_idx % 300:
                print(
                    f"Epoch: {epoch+1:04d}/{num_epochs:04d} | Batch {batch_idx:04d}/{len(train_loader):04d} | Loss: {outputs['loss']:.4f}"
                )

            model.eval()
            with torch.no_grad():
                predicted_labels = torch.argmax(outputs["logits"], 1)
                train_acc.update(predicted_labels, batch["label"])

        ### MORE LOGGING
        with torch.no_grad():
            model.eval()
            val_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2).to(device)
            for batch in val_loader:
                for s in ["input_ids", "attention_mask", "label"]:
                    batch[s] = batch[s].to(device)
                outputs = model(
                    batch["input_ids"],
                    attention_mask=batch["attention_mask"],
                    labels=batch["label"],
                )
                predicted_labels = torch.argmax(outputs["logits"], 1)
                val_acc.update(predicted_labels, batch["label"])

            print(
                f"Epoch: {epoch+1:04d}/{num_epochs:04d} | Train acc.: {train_acc.compute()*100:.2f}% | Val acc.: {val_acc.compute()*100:.2f}%"
            )

    print(watermark(packages="torch,lightning,transformers", python=True))
    print("Torch CUDA available?", torch.cuda.is_available())
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    torch.manual_seed(123)

    ##########################
    ### 1 Loading the Dataset
    ##########################
    download_dataset()
    df = load_dataset_into_to_dataframe()
    if not (op.exists("train.csv") and op.exists("val.csv") and op.exists("test.csv")):
        partition_dataset(df)

    imdb_dataset = load_dataset(
        "csv",
        data_files={
            "train": "train.csv",
            "validation": "val.csv",
            "test": "test.csv",
        },
    )

    #########################################
    ### 2 Tokenization and Numericalization
    #########################################

    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    print("Tokenizer input max length:", tokenizer.model_max_length, flush=True)
    print("Tokenizer vocabulary size:", tokenizer.vocab_size, flush=True)

    print("Tokenizing ...", flush=True)
    imdb_tokenized = imdb_dataset.map(tokenize_text, batched=True, batch_size=None)
    del imdb_dataset
    imdb_tokenized.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    #########################################
    ### 3 Set Up DataLoaders
    #########################################

    train_dataset = IMDBDataset(imdb_tokenized, partition_key="train")
    val_dataset = IMDBDataset(imdb_tokenized, partition_key="validation")
    test_dataset = IMDBDataset(imdb_tokenized, partition_key="test")

    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=12,
        shuffle=True,
        num_workers=1,
        drop_last=True,
    )

    val_loader = DataLoader(
        dataset=val_dataset,
        batch_size=12,
        num_workers=1,
        drop_last=True,
    )

    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=12,
        num_workers=1,
        drop_last=True,
    )

    #########################################
    ### 4 Initializing the Model
    #########################################

    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased", num_labels=2
    )

    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)

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
        device=device,
    )

    end = time.time()
    elapsed = end - start
    print(f"Time elapsed {elapsed/60:.2f} min")

    with torch.no_grad():
        model.eval()
        test_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2).to(device)
        for batch in test_loader:
            for s in ["input_ids", "attention_mask", "label"]:
                batch[s] = batch[s].to(device)
            outputs = model(
                batch["input_ids"],
                attention_mask=batch["attention_mask"],
                labels=batch["label"],
            )
            predicted_labels = torch.argmax(outputs["logits"], 1)
            test_acc.update(predicted_labels, batch["label"])

    print(f"Test accuracy {test_acc.compute()*100:.2f}%")
```

（你也可以在 GitHub 上找到这段代码：[1\_pytorch-distilbert.py](https://github.com/rasbt/faster-pytorch-blog/blob/main/1_pytorch-distilbert.py)。）

为了让文章主题集中，我会略过 PyTorch 基础，只重点描述这个脚本的大致结构。不过，如果你刚接触 PyTorch，我推荐去看看我的免费[深度学习基础课程](https://lightning.ai/pages/courses/deep-learning-fundamentals/)（Deep Learning Fundamentals），其中第 1-4 单元非常详细地讲解了 PyTorch。

上面的代码分为两部分：函数定义，以及在 `if __name__ == "__main__"` 下执行的代码。这种推荐的结构是必要的，可以避免稍后使用多 GPU 时 Python 多进程带来的问题。

`if __name__ == "__main__"` 部分的前三节包含设置数据加载器的代码。第四节用于初始化模型：一个将要微调的预训练 DistilBERT 模型。然后，在第五节中，我们运行训练函数，并在测试集上评估微调后的模型。

在 A100 GPU 上运行这段代码后，我得到了如下结果：

```python
Epoch: 0001/0003 | Batch 0000/2916 | Loss: 0.6867
Epoch: 0001/0003 | Batch 0300/2916 | Loss: 0.3633
Epoch: 0001/0003 | Batch 0600/2916 | Loss: 0.4122
Epoch: 0001/0003 | Batch 0900/2916 | Loss: 0.3046
Epoch: 0001/0003 | Batch 1200/2916 | Loss: 0.3859
Epoch: 0001/0003 | Batch 1500/2916 | Loss: 0.4489
Epoch: 0001/0003 | Batch 1800/2916 | Loss: 0.5721
Epoch: 0001/0003 | Batch 2100/2916 | Loss: 0.6470
Epoch: 0001/0003 | Batch 2400/2916 | Loss: 0.3116
Epoch: 0001/0003 | Batch 2700/2916 | Loss: 0.2002
Epoch: 0001/0003 | Train acc.: 89.81% | Val acc.: 92.17%
Epoch: 0002/0003 | Batch 0000/2916 | Loss: 0.0935
Epoch: 0002/0003 | Batch 0300/2916 | Loss: 0.0674
Epoch: 0002/0003 | Batch 0600/2916 | Loss: 0.1279
Epoch: 0002/0003 | Batch 0900/2916 | Loss: 0.0686
Epoch: 0002/0003 | Batch 1200/2916 | Loss: 0.0104
Epoch: 0002/0003 | Batch 1500/2916 | Loss: 0.0888
Epoch: 0002/0003 | Batch 1800/2916 | Loss: 0.1151
Epoch: 0002/0003 | Batch 2100/2916 | Loss: 0.0648
Epoch: 0002/0003 | Batch 2400/2916 | Loss: 0.0656
Epoch: 0002/0003 | Batch 2700/2916 | Loss: 0.0354
Epoch: 0002/0003 | Train acc.: 95.02% | Val acc.: 92.09%
Epoch: 0003/0003 | Batch 0000/2916 | Loss: 0.0143
Epoch: 0003/0003 | Batch 0300/2916 | Loss: 0.0108
Epoch: 0003/0003 | Batch 0600/2916 | Loss: 0.0228
Epoch: 0003/0003 | Batch 0900/2916 | Loss: 0.0140
Epoch: 0003/0003 | Batch 1200/2916 | Loss: 0.0220
Epoch: 0003/0003 | Batch 1500/2916 | Loss: 0.0123
Epoch: 0003/0003 | Batch 1800/2916 | Loss: 0.0495
Epoch: 0003/0003 | Batch 2100/2916 | Loss: 0.0039
Epoch: 0003/0003 | Batch 2400/2916 | Loss: 0.0168
Epoch: 0003/0003 | Batch 2700/2916 | Loss: 0.1293
Epoch: 0003/0003 | Train acc.: 97.28% | Val acc.: 89.88%
Time elapsed 21.33 min
Test accuracy 89.92%
```

从上面的输出可以看到，模型从第 2 轮到第 3 轮开始轻微过拟合，验证准确率从 92.09% 下降到 89.88%。最终测试准确率为 89.92%，这是微调 21.33 分钟后得到的结果。

## 2) 使用 Trainer 类

现在，我们把 PyTorch 模型包装进 `LightningModule`，以便使用 Lightning 提供的 `Trainer` 类：

```python
import os
import os.path as op
import time

from datasets import load_dataset
import lightning as L
from lightning.pytorch.callbacks import ModelCheckpoint
from lightning.pytorch.loggers import CSVLogger
import matplotlib.pyplot as plt
import pandas as pd
import torch
from torch.utils.data import DataLoader
import torchmetrics
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from watermark import watermark

from local_dataset_utilities import (
    download_dataset,
    load_dataset_into_to_dataframe,
    partition_dataset,
)
from local_dataset_utilities import IMDBDataset

def tokenize_text(batch):
    return tokenizer(batch["text"], truncation=True, padding=True)

class LightningModel(L.LightningModule):
    def __init__(self, model, learning_rate=5e-5):
        super().__init__()

        self.learning_rate = learning_rate
        self.model = model

        self.train_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2)
        self.val_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2)
        self.test_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2)

    def forward(self, input_ids, attention_mask, labels):
        return self.model(input_ids, attention_mask=attention_mask, labels=labels)

    def training_step(self, batch, batch_idx):
        outputs = self(
            batch["input_ids"],
            attention_mask=batch["attention_mask"],
            labels=batch["label"],
        )
        self.log("train_loss", outputs["loss"])
        with torch.no_grad():
            logits = outputs["logits"]
            predicted_labels = torch.argmax(logits, 1)
            self.train_acc(predicted_labels, batch["label"])
            self.log("train_acc", self.train_acc, on_epoch=True, on_step=False)
        return outputs["loss"]  # this is passed to the optimizer for training

    def validation_step(self, batch, batch_idx):
        outputs = self(
            batch["input_ids"],
            attention_mask=batch["attention_mask"],
            labels=batch["label"],
        )
        self.log("val_loss", outputs["loss"], prog_bar=True)

        logits = outputs["logits"]
        predicted_labels = torch.argmax(logits, 1)
        self.val_acc(predicted_labels, batch["label"])
        self.log("val_acc", self.val_acc, prog_bar=True)

    def test_step(self, batch, batch_idx):
        outputs = self(
            batch["input_ids"],
            attention_mask=batch["attention_mask"],
            labels=batch["label"],
        )

        logits = outputs["logits"]
        predicted_labels = torch.argmax(logits, 1)
        self.test_acc(predicted_labels, batch["label"])
        self.log("accuracy", self.test_acc, prog_bar=True)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(
            self.trainer.model.parameters(), lr=self.learning_rate
        )
        return optimizer

if __name__ == "__main__":
    print(watermark(packages="torch,lightning,transformers", python=True), flush=True)
    print("Torch CUDA available?", torch.cuda.is_available(), flush=True)

    torch.manual_seed(123)

    ##########################
    ### 1 Loading the Dataset
    ##########################
    download_dataset()
    df = load_dataset_into_to_dataframe()
    if not (op.exists("train.csv") and op.exists("val.csv") and op.exists("test.csv")):
        partition_dataset(df)

    imdb_dataset = load_dataset(
        "csv",
        data_files={
            "train": "train.csv",
            "validation": "val.csv",
            "test": "test.csv",
        },
    )

    #########################################
    ### 2 Tokenization and Numericalization
    ########################################

    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    print("Tokenizer input max length:", tokenizer.model_max_length, flush=True)
    print("Tokenizer vocabulary size:", tokenizer.vocab_size, flush=True)

    print("Tokenizing ...", flush=True)
    imdb_tokenized = imdb_dataset.map(tokenize_text, batched=True, batch_size=None)
    del imdb_dataset
    imdb_tokenized.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    #########################################
    ### 3 Set Up DataLoaders
    #########################################

    train_dataset = IMDBDataset(imdb_tokenized, partition_key="train")
    val_dataset = IMDBDataset(imdb_tokenized, partition_key="validation")
    test_dataset = IMDBDataset(imdb_tokenized, partition_key="test")

    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=12,
        shuffle=True,
        num_workers=1,
        drop_last=True,
    )

    val_loader = DataLoader(
        dataset=val_dataset,
        batch_size=12,
        num_workers=1,
        drop_last=True,
    )

    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=12,
        num_workers=1,
        drop_last=True,
    )

    #########################################
    ### 4 Initializing the Model
    #########################################

    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased", num_labels=2
    )

    #########################################
    ### 5 Finetuning
    #########################################

    lightning_model = LightningModel(model)

    callbacks = [
        ModelCheckpoint(save_top_k=1, mode="max", monitor="val_acc")  # save top 1 model
    ]
    logger = CSVLogger(save_dir="logs/", name="my-model")

    trainer = L.Trainer(
        max_epochs=3,
        callbacks=callbacks,
        accelerator="gpu",
        devices=[1],
        logger=logger,
        log_every_n_steps=10,
        deterministic=True,
    )

    start = time.time()
    trainer.fit(
        model=lightning_model,
        train_dataloaders=train_loader,
        val_dataloaders=val_loader,
    )

    end = time.time()
    elapsed = end - start
    print(f"Time elapsed {elapsed/60:.2f} min")

    test_acc = trainer.test(lightning_model, dataloaders=test_loader, ckpt_path="best")
    print(test_acc)

    with open(op.join(trainer.logger.log_dir, "outputs.txt"), "w") as f:
        f.write((f"Time elapsed {elapsed/60:.2f} min\n"))
        f.write(f"Test acc: {test_acc}")
```

（你也可以在 GitHub 上找到这段代码：[2\_pytorch-with-trainer.py](https://github.com/rasbt/faster-pytorch-blog/blob/main/2_pytorch-with-trainer.py)。）

同样，为了保持本文对性能主题的聚焦，我会略过 `LightningModule` 的细节。不过，我会在[深度学习基础课程](https://lightning.ai/pages/courses/deep-learning-fundamentals/)的第 5 单元（计划 3 月上线）中更详细地讲解 `LightningModule` 和 `Trainer` 类。在此之前，推荐阅读[官方 PyTorch Lightning 教程](https://pytorch-lightning.readthedocs.io/en/stable/starter/introduction.html)。

简而言之，我们搭建了一个 `LightningModule`，它定义了训练、验证和测试步骤各自如何执行。主要的改动位于代码第 5 节，也就是微调模型的地方：现在我们把 PyTorch 模型包装进 `LightningModel` 类，并使用 `Trainer` 类来训练模型：

```python
    #########################################
    ### 5 Finetuning
    #########################################

    lightning_model = LightningModel(model)

    callbacks = [
        ModelCheckpoint(save_top_k=1, mode="max", monitor="val_acc")  # save top 1 model
    ]
    logger = CSVLogger(save_dir="logs/", name="my-model")

    trainer = L.Trainer(
        max_epochs=3,
        callbacks=callbacks,
        accelerator="gpu",
        devices=1,
        logger=logger,
        log_every_n_steps=10,
        deterministic=True,
    )

    trainer.fit(
        model=lightning_model,
        train_dataloaders=train_loader,
        val_dataloaders=val_loader,
    )
```

由于我们之前注意到验证准确率从第 2 轮到第 3 轮有所下降，我们使用 `ModelCheckpoint` 回调来加载最佳模型（以验证准确率最高为准），再在测试集上做模型评估。此外，我们还会把性能记录到 CSV 文件（我偏好的记录方式），并把 PyTorch 的行为设置为确定性（deterministic）。

在同一台机器上，这个模型在 21.79 分钟内达到了 92.6% 的测试准确率：

![Pytorch 提速：Trainer](https://sebastianraschka.com/images/blog/2023/pytorch-faster/2-trainer.webp)

注意，如果禁用检查点保存（checkpointing）并让 PyTorch 以非确定性模式运行，运行时间将与纯 PyTorch 相同。

![Pytorch 提速：基准 1](https://sebastianraschka.com/images/blog/2023/pytorch-faster/benchmark-1.webp)

## 3) [自动混合精度](https://sebastianraschka.com/glossary/#mixed-precision "Mixed Precision")训练

如果你的 GPU 支持混合精度训练，启用它往往是提升计算效率的主要手段之一。具体而言，我们使用自动混合精度训练，它在训练过程中在 32 位和 16 位浮点表示之间自动切换，且不会牺牲精度。

![Pytorch 提速：混合精度](https://sebastianraschka.com/images/blog/2023/pytorch-faster/mixed-precision.webp)

使用 `Trainer` 类，只需一行代码即可启用自动混合精度训练：

```python
    trainer = L.Trainer(
        max_epochs=3,
        callbacks=callbacks,
        accelerator="gpu",
        precision="16",  # <-- NEW
        devices=[1],
        logger=logger,
        log_every_n_steps=10,
        deterministic=True,
    )
```

如上所示，使用混合精度训练把训练时间从 21.79 分钟缩短到 8.25 分钟！速度几乎提升了 3 倍！

测试集准确率为 93.2%——比之前的 92.6% 还略有提升（这很可能是不同精度模式之间切换时由舍入带来的差异所致）。

![Pytorch 提速：基准 2](https://sebastianraschka.com/images/blog/2023/pytorch-faster/benchmark-2.webp)

## 4) 使用 [Torch.Compile](https://sebastianraschka.com/glossary/#torch-compile "torch.compile") 的静态图

在[不久前发布的 PyTorch 2.0 公告](https://pytorch.org/get-started/pytorch-2.0/)中，PyTorch 团队推出了新的 `toch.compile` 函数，它通过生成优化后的静态图来加速 PyTorch 代码的执行，而不是以动态图（即所谓的 *eager* 模式）运行 PyTorch 代码。其底层实现是一个三步过程：获取图（graph acquisition）、降低图（graph lowering）和编译图（graph compilation）。

![Pytorch 提速：PyTorch 2.0 图 4](https://sebastianraschka.com/images/blog/2023/pytorch-faster/pytorch-2.0-img4.webp)

（图片来源：<https://pytorch.org/get-started/pytorch-2.0/>）

这一特性背后有许多精巧的实现细节，[PyTorch 2.0 公告](https://pytorch.org/get-started/pytorch-2.0/)对此有更详细的解释。作为用户，我们只需一条简单的命令 `torch.compile` 即可使用这个新特性。

要利用 `torch.compile`，我们只需在代码中加上这一行：

```python
# ...
model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased", num_labels=2
    )

model = torch.compile(model) # NEW
lightning_model = LightningModel(model)
# ...
```

（关于 `torch.compile` 函数的更多细节，另请参阅官方的 [torch.compile 教程](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)）

遗憾的是，在使用默认参数的情况下，`torch.compile` 似乎并没有在这一混合精度场景下给 DistilBERT 模型带来性能提升。训练时间为 8.44 分钟，而之前是 8.25 分钟。因此，本教程后续的基准测试将不再使用 `torch.compile`。

![Pytorch 提速：基准 3](https://sebastianraschka.com/images/blog/2023/pytorch-faster/benchmark-3.webp)

---

**附注：** 如果应用下面两个技巧，

1. 把编译放在计时开始之前；
2. 用一个示例 batch 对模型进行"预热"（priming），如下所示

```python
  model.to(torch.device("cuda:0"))
  model = torch.compile(model)

  for batch_idx, batch in enumerate(train_loader):
      model.train()
      for s in ["input_ids", "attention_mask", "label"]:
          batch[s] = batch[s].to(torch.device("cuda:0"))
      break

  outputs = model(
      batch["input_ids"],
      attention_mask=batch["attention_mask"],
      labels=batch["label"],
  )

  lightning_model = LightningModel(model)
  # start timing and training below
```

运行时间就能改善到 5.6 分钟。这说明初始的优化编译步骤需要几分钟，但最终会加速模型训练。在本例中，由于我们只训练 3 个 epoch，额外的开销掩盖了编译带来的收益。不过，如果训练时间更长或模型更大，编译就是值得的。

（注意：在分布式设置下对模型做预热目前有些棘手，因为每个 GPU 设备都需要一份模型副本。这需要对代码做一些重构，我可能会在以后再回头处理，因此下面的代码将不使用 `torch.compile`。）

---

## 5) 使用分布式数据并行在 4 块 GPU 上训练

上面我们通过混合精度训练（并尝试了图编译）来加速单 GPU 上的代码，现在让我们来探索多 GPU 策略。具体而言，我们将在 4 块而非 1 块 GPU 上运行同样的代码。

注意，业界有多种不同的多 GPU 训练技术，我在下图中做了总结。

为了保持这篇博文的简洁与聚焦，关于不同多 GPU 训练范式的更多细节，推荐阅读我的《[Machine Learning Q and AI](https://leanpub.com/machine-learning-q-and-ai/)》一书，该章节已包含在免费预览版中。此外，我也会在深度学习基础课程的第 9 单元（计划 4 月发布）中讲解这些内容。

![Pytorch 提速：多 GPU](https://sebastianraschka.com/images/blog/2023/pytorch-faster/multi-gpu.webp)

我们从最简单的技术开始：通过 `DistributedDataParallel` 实现数据并行。使用 `Trainer`，我们只需修改一行代码：

```python
    trainer = L.Trainer(
        max_epochs=3,
        callbacks=callbacks,
        accelerator="gpu",
        devices=4,  # <-- NEW
        strategy="ddp",  # <-- NEW
        precision="16",
        logger=logger,
        log_every_n_steps=10,
        deterministic=True,
    )
```

在我的机器上（配备 4 块 A100 GPU），这段代码运行了 3.07 分钟，测试准确率达到 93.1%。测试集成绩的提升同样很可能来自数据并行时的梯度平均。

![Pytorch 提速：基准 4](https://sebastianraschka.com/images/blog/2023/pytorch-faster/benchmark-4.webp)

（详细讲解数据并行是未来文章的又一个好题材。）

![Pytorch 提速：DDP](https://sebastianraschka.com/images/blog/2023/pytorch-faster/ddp.webp)

## 6) DeepSpeed

最后，让我们探索可以在 `Trainer` 中使用的 [DeepSpeed](https://github.com/microsoft/DeepSpeed) 多 GPU 策略。

但在实际尝试之前，我想先分享我的多 GPU 使用建议。选择哪种策略主要取决于模型本身、GPU 数量以及 GPU 的显存大小。例如，在[预训练](https://sebastianraschka.com/glossary/#pretraining "Pretraining")大到单块 GPU 装不下的大模型时，一个不错的起点是简单的 `"ddp_sharded"` 策略，它在 `"ddp"` 的基础上增加了张量并行。使用前面的代码，`"ddp_sharded"` 运行需要 2.58 分钟。

另外，我们也可以考虑更精细的 `"deepspeed_stage_2"` 策略，它会对优化器状态和梯度进行分片（shard）。如果这样仍不足以把模型装进 GPU 显存，可以试试 `"deepspeed_stage_2_offload"` 变体，它把优化器状态和梯度卸载（offload）到 CPU 内存（以牺牲一些性能为代价）。关于 DeepSpeed 策略及其 ZeRO（零冗余优化器）的更多信息，请参阅官方的 [ZeRO 教程](https://www.deepspeed.ai/tutorials/zero/)；关于卸载的更多信息，请参阅 [ZeRO offload 教程](https://www.deepspeed.ai/tutorials/zero-offload/)。

回到建议本身：如果你要微调模型，相比计算吞吐量，能否把模型装进更少数量的 GPU 的显存通常是更值得关注的问题。这种情况下，你可以探索 deepspeed 的 `"stage_3"` 变体，它对一切内容——优化器、梯度和参数——都做分片，即：

- `strategy="deepspeed_stage_3"`
- `strategy="deepspeed_stage_3_offload"`

由于像 DistilBERT 这样的小模型不存在显存问题，我们来试试 `"deepspeed_stage_2"`：

首先，我们需要安装 DeepSpeed Python 库：

```python
pip install -U deepspeed
```

（在我的机器上，这安装的是 deepspeed-0.8.2。）

接下来，只需改动一行代码即可启用 `"deepspeed_stage_2"`：

```python
    trainer = L.Trainer(
        max_epochs=3,
        callbacks=callbacks,
        accelerator="gpu",
        devices=4,
        strategy="deepspeed_stage_2",  # <-- NEW
        precision="16",
        logger=logger,
        log_every_n_steps=10,
        deterministic=True,
    )
```

在我的机器上运行耗时 2.75 分钟，测试准确率达到 92.6%。

注意，PyTorch 如今也有了 DeepSpeed 的自家替代方案，名为 fully-sharded DataParallel（全分片数据并行），我们可以通过 `strategy="fsdp"` 来使用它。

![Pytorch 提速：基准 5](https://sebastianraschka.com/images/blog/2023/pytorch-faster/benchmark-5.webp)

## 7) Fabric

随着近期的 Lightning 2.0 发布，Lightning AI 推出了新的 [Fabric 开源库（面向 PyTorch）](https://lightning.ai/docs/fabric/stable/)。Fabric 本质上是在不使用 `LightningModule` 和 `Trainer`（即上文*2) 使用 Trainer 类*一节介绍的方式）的情况下扩展 PyTorch 代码的另一种途径。

Fabric 只需要改动几行代码，如下方代码所示。`-` 表示被移除的行，`+` 表示为把 Python 代码改造成使用 Fabric 而新增的行。

```python
import os
import os.path as op
import time

+ from lightning import Fabric

from datasets import load_dataset
import matplotlib.pyplot as plt
import pandas as pd
import torch
from torch.utils.data import DataLoader
import torchmetrics
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from watermark import watermark

from local_dataset_utilities import download_dataset, load_dataset_into_to_dataframe, partition_dataset
from local_dataset_utilities import IMDBDataset

def tokenize_text(batch):
    return tokenizer(batch["text"], truncation=True, padding=True)

def plot_logs(log_dir):
    metrics = pd.read_csv(op.join(log_dir, "metrics.csv"))

    aggreg_metrics = []
    agg_col = "epoch"
    for i, dfg in metrics.groupby(agg_col):
        agg = dict(dfg.mean())
        agg[agg_col] = i
        aggreg_metrics.append(agg)

    df_metrics = pd.DataFrame(aggreg_metrics)
    df_metrics[["train_loss", "val_loss"]].plot(
        grid=True, legend=True, xlabel="Epoch", ylabel="Loss"
    )
    plt.savefig(op.join(log_dir, "loss.pdf"))

    df_metrics[["train_acc", "val_acc"]].plot(
        grid=True, legend=True, xlabel="Epoch", ylabel="Accuracy"
    )
    plt.savefig(op.join(log_dir, "acc.pdf"))

- def train(num_epochs, model, optimizer, train_loader, val_loader, device):
+ def train(num_epochs, model, optimizer, train_loader, val_loader, fabric):

      for epoch in range(num_epochs):
-         train_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2).to(device)
+         train_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2).to(fabric.device)

        model.train()
        for batch_idx, batch in enumerate(train_loader):

-             for s in ["input_ids", "attention_mask", "label"]:
-                 batch[s] = batch[s].to(device)

            outputs = model(batch["input_ids"], attention_mask=batch["attention_mask"], labels=batch["label"]) 
            optimizer.zero_grad()
-            outputs["loss"].backward()
+            fabric.backward(outputs["loss"])

            ### UPDATE MODEL PARAMETERS
            optimizer.step()

            ### LOGGING
            if not batch_idx % 300:
                print(f"Epoch: {epoch+1:04d}/{num_epochs:04d} | Batch {batch_idx:04d}/{len(train_loader):04d} | Loss: {outputs['loss']:.4f}")

            model.eval()
            with torch.no_grad():
                predicted_labels = torch.argmax(outputs["logits"], 1)
                train_acc.update(predicted_labels, batch["label"])

        ### MORE LOGGING
        model.eval()
        with torch.no_grad():
-            val_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2).to(device)
+            val_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2).to(fabric.device)
            for batch in val_loader:
-                for s in ["input_ids", "attention_mask", "label"]:
-                    batch[s] = batch[s].to(device)
                outputs = model(batch["input_ids"], attention_mask=batch["attention_mask"], labels=batch["label"])
                predicted_labels = torch.argmax(outputs["logits"], 1)
                val_acc.update(predicted_labels, batch["label"])

            print(f"Epoch: {epoch+1:04d}/{num_epochs:04d} | Train acc.: {train_acc.compute()*100:.2f}% | Val acc.: {val_acc.compute()*100:.2f}%")
            train_acc.reset(), val_acc.reset()

if __name__ == "__main__":

    print(watermark(packages="torch,lightning,transformers", python=True))
    print("Torch CUDA available?", torch.cuda.is_available())    
-   device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(123)

    ##########################
    ### 1 Loading the Dataset
    ##########################
    download_dataset()
    df = load_dataset_into_to_dataframe()
    if not (op.exists("train.csv") and op.exists("val.csv") and op.exists("test.csv")):
        partition_dataset(df)

    imdb_dataset = load_dataset(
        "csv",
        data_files={
            "train": "train.csv",
            "validation": "val.csv",
            "test": "test.csv",
        },
    )

    #########################################
    ### 2 Tokenization and Numericalization
    #########################################

    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    print("Tokenizer input max length:", tokenizer.model_max_length, flush=True)
    print("Tokenizer vocabulary size:", tokenizer.vocab_size, flush=True)

    print("Tokenizing ...", flush=True)
    imdb_tokenized = imdb_dataset.map(tokenize_text, batched=True, batch_size=None)
    del imdb_dataset
    imdb_tokenized.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    #########################################
    ### 3 Set Up DataLoaders
    #########################################

    train_dataset = IMDBDataset(imdb_tokenized, partition_key="train")
    val_dataset = IMDBDataset(imdb_tokenized, partition_key="validation")
    test_dataset = IMDBDataset(imdb_tokenized, partition_key="test")

    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=12,
        shuffle=True, 
        num_workers=2,
        drop_last=True,
    )

    val_loader = DataLoader(
        dataset=val_dataset,
        batch_size=12,
        num_workers=2,
        drop_last=True,
    )

    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=12,
        num_workers=2,
        drop_last=True,
    )

    #########################################
    ### 4 Initializing the Model
    #########################################

+    fabric = Fabric(accelerator="cuda", devices=4, 
+                    strategy="deepspeed_stage_2", precision="16-mixed")
+    fabric.launch()

    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased", num_labels=2)

-   model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)

+    model, optimizer = fabric.setup(model, optimizer)
+    train_loader, val_loader, test_loader = fabric.setup_dataloaders(
+        train_loader, val_loader, test_loader)

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
-       device=device
+       fabric=fabric
    )

    end = time.time()
    elapsed = end-start
    print(f"Time elapsed {elapsed/60:.2f} min")

    with torch.no_grad():
        model.eval()
-       test_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2).to(device)
+       test_acc = torchmetrics.Accuracy(task="multiclass", num_classes=2).to(fabric.device)
        for batch in test_loader:
-           for s in ["input_ids", "attention_mask", "label"]:
-               batch[s] = batch[s].to(device)
            outputs = model(batch["input_ids"], attention_mask=batch["attention_mask"], labels=batch["label"])
            predicted_labels = torch.argmax(outputs["logits"], 1)
            test_acc.update(predicted_labels, batch["label"])

    print(f"Test accuracy {test_acc.compute()*100:.2f}%")
```

可以看到，改动非常轻量！运行效果如何？Fabric 仅用 1.8 分钟就完成了微调！Fabric 比 Trainer 更轻量——尽管它同样支持回调（callback）和日志功能，但这里为了用一个极简示例展示 Fabric，我们没有启用这些特性。快得飞起，对吧？

![Pytorch 提速：最终基准](https://sebastianraschka.com/images/blog/2023/pytorch-faster/benchmark-last.webp)

选用 Lightning Trainer 还是 Fabric 取决于个人偏好。经验法则是：如果你希望在现有 PyTorch 代码外面套一层轻量封装，就用 Fabric；反之，如果你转向更大的项目、更看重 Lightning 提供的代码组织方式，我推荐使用 Trainer。

## 结论

本文探索了多种提升 PyTorch 模型训练速度的技术。如果使用 Lightning Trainer，我们只需一行代码就能在这些选项之间切换，非常方便——尤其是在调试代码时需要在 CPU 与 GPU 机器之间来回切换的场景。

还有一个尚未探索的方面是最大化 batch size，它可以进一步提升模型的吞吐量。不过，这个优化就留到以后再说吧。

[如果你想亲自运行这些代码，我把它们都分享在了 GitHub 上](https://github.com/rasbt/faster-pytorch-blog)
