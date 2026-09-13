---
title: "PyTorch DataPipes 与 DataLoader"
title_en: "PyTorch DataPipes and DataLoaders"
source: https://sebastianraschka.com/blog/2022/datapipes.html
crawled: 2026-09-06
translated: 2026-09-06
---

# PyTorch DataPipes 与 DataLoader

> 原文：[PyTorch DataPipes and DataLoaders](https://sebastianraschka.com/blog/2022/datapipes.html)

PyTorch 团队[最近发布了](https://pytorch.org/data/beta/index.html) TorchData，这是一个专注于为 PyTorch 实现可组合、可复用数据加载工具的原型库。具体来说，[TorchData 库](https://github.com/pytorch/data)围绕 DataPipes 展开，它旨在成为现有 Dataset 类的、与 DataLoader 兼容的替代品。

说实话，我并不讨厌 PyTorch 现有的 [Dataset](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader) 和 [DataLoader](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader) 工具，但我也喜欢尝试新事物。所以在这篇文章中，我在试用了新的 DataPipe API 之后，尝试提供一些简洁的示例以及一些思考。

配套的代码文件可以在 GitHub 上的[这里](https://github.com/rasbt/datapipes-blog)找到。代码最初在以下环境下开发和测试：

```python
Python version: 3.8.13

torch: 1.11.0
torchdata: 0.3.0
```

- [数据加载？有什么大不了的？](#DataLoadingWhatstheBigDeal)
- [准备工作](#SettingtheStage)
- [Dataset 与 DataLoader](#DatasetDataLoader)
  - [步骤 1：定义自定义 Dataset](#Step1:DefiningaCustomDataset)
  - [步骤 2：实例化训练集、验证集和测试集](#Step2:InstantiatingTrainingValidationandTestsets)
  - [步骤 3：创建 DataLoader](#Step3:CreatingDataLoaders)
  - [步骤 4：试用 DataLoader](#Step4:TryingtheDataLoaders)
- [使用 ImageFolder 创建数据集](#CreatingDatasetswithImageFolder)
- [DataPipes 入门](#IntroductiontoDataPipes)
  - [类构造器与函数式形式](#ClassConstructorsandFunctionalForms)
  - [IterDataPipes 与 MapDataPipes](#IterDataPipesandMapDataPipes)
- [用于图像与 CSV 数据集的 DataPipes](#DataPipesforDatasetsWithImagesandCSVs)
  - [已知注意事项](#KnownCaveats)
- [结论](#Conclusions)
  - [哪个更方便？](#WhichIsMoreConvenient)
  - [哪个性能更好？](#WhichIsMorePerformant)
  - [该用哪个？](#WhichShouldYouUse)

## 数据加载？有什么大不了的？

谁不希望深度学习模型训练得更快呢？当然，影响训练时间的因素有很多，比如模型架构、数据点数量、批大小（batch size）、GPU、存储驱动器等等，不胜枚举。

然而，我们要确保数据加载不会成为瓶颈，尤其是在我们花钱买了或租了那块高端 GPU 的情况下。换句话说，我们要确保 GPU 永远不必等待新的一批数据。

让我们用一个例子来说明这个问题。假设我们有如下 PyTorch 训练循环设置：

```python
for epoch in range(num_epochs):
  
    inputs = []
    # prepare next minibatch
    for f in filename_minibatch:
        img = Image.open(os.path.join(img_dir, f))
        img_tensor = o_tensor(img).to('cuda')
        inputs.append(img_tensor)
    inputs = torch.cat(inputs)
    
    # train model 
    logits = model(inputs)
    ...
    loss.backward()
    optimizer.step()
```

这很糟糕！为什么？因为训练和数据加载在同一个 for 循环中按顺序进行。每次加载下一个小批量（minibatch）时，模型和 GPU 都在闲置。

上面的代码造成了数据瓶颈：模型（和 GPU）在等待下一批数据，如下图所示：

![A not ideal data flow where the GPU and model wait for the next batch of data.](https://sebastianraschka.com/images/blog/2022/datapipes/dataflow-bad.webp)

在理想情况下，我们希望模型在反向调用和参数更新（通过 `.step()`）之后立即处理下一个小批量。换句话说，目标是让下一个小批量和模型一样随时就绪，因此我们希望在模型训练的同时在后台持续加载小批量。遗憾的是，由于 Python 有全局解释器锁（GIL），默认只允许运行单个进程，我们将不得不编写复杂的变通方案。

所幸，已经有人替我们解决了这个问题：我们可以使用 PyTorch 的 DataLoader，它做的正是这件事。DataLoader 允许我们指定用于加载后续小批量的后台进程数量，从而不让 GPU 停滞。下图说明了这一点，其中步骤 1 和步骤 2 是并行运行的独立进程。这里的思路是：始终有多个训练样本（"x, y"）可供模型在下一轮取用——理论上有一个就够了。

![An ideal data flow with data loading in the background so the GPU and model are not idle.](https://sebastianraschka.com/images/blog/2022/datapipes/dataflow-good.webp)

通常，我们把 `Dataset` 类和 `DataLoader` 类一起使用。我们在 Dataset 实例中定义数据文件如何打开，而 DataLoader 则帮助我们：

- 打乱数据，
- 把数据整理成小批量，
- 使用多个进程在后台准备小批量，
- 以及更多。

DataPipes 的一个目标是提供一些可复用的组件，以便更灵活地构建 Dataset。另一个目标是简化 DataLoader。目前，DataLoader 的逻辑相对复杂，要做很多事情。其中部分功能将被编码进 DataPipe 本身，这为未来 PyTorch 版本中出现新的 DataLoader2 铺平了道路。

（注意，截至本文撰写时，TorchData 库中已经有 `DataLoader2` 的原型，可以在[这里](https://github.com/pytorch/data/blob/main/torchdata/dataloader2/dataloader2.py#L46)找到——感谢 [Elijah Rippeth](https://twitter.com/terrible_coder) 指出这一点。不过，目前使用 DataPipes 的主要方式仍然是将其与现有的 DataLoader 结合。另外，PyTorch 团队打算保留原有的 Dataset 和 DataLoader，所以你不必急着采用 DataPipes。）

在本文中，我们首先看看当前如何把 Dataset 与 DataLoader 一起使用。然后，我们将看到如何组合 DataPipes，使其与 DataLoader 一起复现这一行为。

## 准备工作

在接下来的小节中，我们将通过一些动手示例来实现 Dataset、DataLoader 和 DataPipes。为了保持简单，我们将使用无聊但经典的 MNIST 数据集。当然，PyTorch 已经内置了 MNIST 数据集，但那样用就有点作弊了。我们改用一种以单个 PNG 图像文件形式组织的 MNIST 数据集版本，以模拟任意的真实世界深度学习项目——项目里通常有大量文件分布在各种文件夹中。

为了让本文聚焦于要点，我们不会展开获取数据集的代码。不过，如果你想把这个数据集下载到自己的电脑上把玩，可以运行 [0_download-and-prep-data.ipynb](https://github.com/rasbt/datapipes-blog/blob/main/0_download-and-prep-data.ipynb) 这个 Jupyter notebook。运行代码后，应该会有一个 `mnist-png` 文件夹，其中包含两个子文件夹：`train` 和 `test`。这两个子文件夹各自又包含 10 个子文件夹。这些以数字 0-9 命名的子文件夹对应类别标签。每个文件夹里面就是实际的 PNG 文件：

![Datapipes mnist folder](https://sebastianraschka.com/images/blog/2022/datapipes/mnist-folder.webp)

训练集应该有 5 万张 PNG，测试集有 1 万张 PNG。

除了子文件夹和 PNG 文件之外，还有三个 CSV 文件：`test.csv`、`new_train.csv` 和 `new_val.csv`。它们分别包含三个数据子集中各个文件的路径和标签。出于说明目的，下面展示了训练集和验证集 CSV 文件的前五行：

![Datapipes csv files](https://sebastianraschka.com/images/blog/2022/datapipes/csv-files.webp)

请注意，MNIST 数据集没有专门的验证集文件夹。为了生成 `new_train.csv` 和 `new_val.csv`，我们把包含 5 万张训练集图像的 CSV 文件拆分为 4.5 万张用于训练、5 千张用于验证，这也是验证集 CSV 的文件路径中同样含有 `train` 的原因。

## Dataset 与 DataLoader

在本节中，我们以传统方式使用 Dataset 和 DataLoader。第 1 步，我们定义包含所有文件加载逻辑的数据集。第 2 步，我们为训练集、验证集和测试集实例化数据集对象。第 3 步，我们实例化数据加载器。第 4 步，我们进行一次测试迭代，以确保数据加载器工作正常。

在深入之前，下图说明了这三个主要步骤的整体流程：

![Datapipes loader flow](https://sebastianraschka.com/images/blog/2022/datapipes/loader-flow.webp)

如果你想自己运行下面的代码，我建议参考本文配套 GitHub 仓库中的独立文件 [1_dataset-csv.py](https://github.com/rasbt/datapipes-blog/blob/main/1_dataset-csv.py)。

### 步骤 1：定义自定义 Dataset

在本节中，我们定义一个用于加载训练样本的自定义 `Dataset` 类。一个数据集通常包含三个方法。

1. `__init__`：构造函数，包含或调用数据集的主要设置代码。
2. `__getitem__`：指定如何加载单个数据实例的方法。
3. `__len__`：返回数据实例总数的方法。

我们来看看下面这个继承自 PyTorch `Dataset` 的 `MyDataset` 类：

```python
import os
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, csv_path, img_dir, transform=None):

        df = pd.read_csv(csv_path)
        self.img_dir = img_dir
        self.transform = transform

        # based on DataFrame columns
        self.img_names = df["filepath"]
        self.labels = df["label"]

    def __getitem__(self, index):
        img = Image.open(os.path.join(self.img_dir, self.img_names[index]))

        if self.transform is not None:
            img = self.transform(img)

        label = self.labels[index]
        return img, label

    def __len__(self):
        return self.labels.shape[0]
```

`__init__` 方法包含使用 Pandas 打开 CSV 文件的代码。它还把 `"filepath"` 和 `"label"` 两列存储为属性，以便稍后在其他 `Dataset` 方法中引用。

`__getitem__` 方法接受一个指向单个数据实例的 `index` 参数。如果我们的数据集由 50,000 个训练样本组成，那么 `index` 就是 0 到 49,999 之间的一个数字。在 `__getitem__` 方法内部，我们用 `index` 通过 `self.img_names[index])` 从文件路径列表中取出文件名，并用 PIL 打开图像。注意，PIL 图像接下来会经过一个可选的变换步骤——如果用 PyTorch 做模型训练，这一步通常至少要转换成 PyTorch 张量数据类型，这个稍后再说。最后，我们取出对应的标签，并返回 "`img, label`" 这一对。

`__len__` 方法比较无趣；它只是返回数据集的长度，也就是我们之前赋给 `self.labels` 的标签列的长度。

总之，我们自定义的 `MyDataset` 类定义了如何打开并返回单个文件。下一节中，我们将实例化自定义的 `MyDataset` 实例。

### 步骤 2：实例化训练集、验证集和测试集

现在我们有了自定义的 `MyDataset` 类，就可以为数据加载器实例化数据集了。在下面的代码中，我们分别为训练、验证和测试创建独立的数据集：

```python
train_dataset = MyDataset(
    csv_path="mnist-pngs/new_train.csv",
    img_dir="mnist-pngs/",
    transform=data_transforms["train"],
)

val_dataset = MyDataset(
    csv_path="mnist-pngs/new_val.csv",
    img_dir="mnist-pngs/",
    transform=data_transforms["test"],
)

test_dataset = MyDataset(
    csv_path="mnist-pngs/test.csv",
    img_dir="mnist-pngs/",
    transform=data_transforms["test"],
)
```

注意，训练集使用的变换步骤（`data_transforms["train"]`）与验证集和测试集（`data_transforms["test"]`）不同。我们来定义这些变换步骤，这样就清楚原因了：

```python
from torchvision import transforms

data_transforms = {
    "train": transforms.Compose(
        [
            transforms.Resize(32),
            transforms.RandomCrop((28, 28)),
            transforms.ToTensor(),
            # normalize images to [-1, 1] range
            transforms.Normalize((0.5,), (0.5,)),
        ]
    ),
    "test": transforms.Compose(
        [
            transforms.Resize(32),
            transforms.CenterCrop((28, 28)),
            transforms.ToTensor(),
            # normalize images to [-1, 1] range
            transforms.Normalize((0.5,), (0.5,)),
        ]
    ),
}
```

这里我们在训练加载器中加入了一些数据变换（`RandomCrop`）。但推理时我们不希望有任何随机性，这就是 `"test"` 变换步骤改用 `CenterCrop` 的原因。（如果省略 `"test"` 变换中的 `CenterCrop`，训练集和测试集图像的分辨率会不一致，这同样不理想。）由于我们用验证集作为训练期间衡量泛化性能的替代品，我建议像对待测试集那样对待它。

最后，简单说一下 `ToTensor` 变换：前面的变换步骤（如 `Resize` 和 `CenterCrop`）作用在 `Dataset` 的`__getitem__` 方法返回的 PIL 图像上。`ToTensor` 变换把 PIL 图像转换为像素值归一化到 0 和 1 之间的 PyTorch 张量。`Normalize` 变换实现 z 分数标准化，即减去均值再除以标准差：\(x' = \frac{x - \mu}{\sigma}.\)

在 `transforms.Normalize((0.5,), (0.5,))` 中，第一个元组包含均值——每个颜色通道一个值。由于 MNIST 是灰度格式，只有一个颜色通道。第二个元组包含标准差。如果是三个颜色通道的 RGB 图像，我们会写成 `transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))`。注意，由于 `ToTensor` 输出的像素值在 [0, 1] 范围内，取 \(\mu=0.5\) 和 \(\sigma=0.5\) 会把像素归一化到 [-1, 1]——这有时能带来更好的梯度下降表现。实践中也建议计算并使用每个通道真实的均值和标准差，但这是另一个话题了。

### 步骤 3：创建 DataLoader

上一步中我们已经实例化了数据集，现在来创建训练集、验证集和测试集的数据加载器：

```python
from torch.utils.data import DataLoader

train_loader = DataLoader(
    dataset=train_dataset,
    batch_size=32,
    shuffle=True,
    drop_last=True,
    transform=data_transforms["train"],
    num_workers=2,
)  

val_loader = DataLoader(
    dataset=val_dataset,
    batch_size=32,
    shuffle=False,
    transform=data_transforms["test"],
    num_workers=2,
)

test_loader = DataLoader(
    dataset=test_dataset,
    batch_size=32,
    shuffle=False,
    transform=data_transforms["test"],
    num_workers=2
)
```

上面，我们用各自对应的数据集实例化了每个数据加载器：`train_dataset` 、 `val_dataset` 和 `test_dataset`。

我们设置 `num_workers=2`，以确保至少有两个子进程用 CPU 并行加载数据（与此同时 GPU 或另一个 CPU 正忙着训练模型）。MNIST 图像非常非常小，所以这种情况下 `num_workers=2` 应该够用了。不过，如果数据集图像更大、数据处理步骤更多，你可能需要考虑分配更多 worker。

验证集和测试集不需要打乱，但我们为训练加载器设置了 `shuffle=True`。这将确保每个轮次（epoch）中训练样本都会被打乱。`drop_last=True` 设置会在数据集不能被批大小整除时丢弃每个 epoch 的最后一批。例如，如果数据集有 45,000 个训练样本、批大小为 32，最后一批就只包含 \(45,000 - 1,406 \times 32 = 8\) 个样本，有时这些小批量会导致梯度更新带噪声，所以我建议训练加载器使用 `drop_last=True`。

注意，`DataLoader` 还有许多其他设置，包括 `pin_memory`、`persistent_workers` 等。我鼓励你去看看[官方 API 文档](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader)。

### 步骤 4：试用 DataLoader

最后，让我们通过迭代前 3 个小批量来检验实现是否正常：

```python
    num_epochs = 1
    for epoch in range(num_epochs):

        for batch_idx, (x, y) in enumerate(train_loader):
            if batch_idx >= 3:
                break
            print(" Batch index:", batch_idx, end="")
            print(" | Batch size:", y.shape[0], end="")
            print(" | x shape:", x.shape, end="")
            print(" | y shape:", y.shape)            

    print("Labels from current batch:", y)
```

上面的代码应该会打印出如下内容（不过请注意，标签可能因你的随机种子设置而不同）：

```python
 Batch index: 0 | Batch size: 32 | x shape: torch.Size([32, 1, 28, 28]) | y shape: torch.Size([32])
 Batch index: 1 | Batch size: 32 | x shape: torch.Size([32, 1, 28, 28]) | y shape: torch.Size([32])
 Batch index: 2 | Batch size: 32 | x shape: torch.Size([32, 1, 28, 28]) | y shape: torch.Size([32])
Labels from current batch: tensor([5, 1, 1, 1, 8, 3, 1, 1, 5, 8, 8, 6, 4, 4, 8, 5, 8, 5, 5, 0, 6, 5, 8, 9,
        4, 9, 6, 9, 0, 8, 5, 8])
```

到目前为止一切顺利，一切似乎都按预期工作。

上面这种"Dataset+CSV 文件"的做法对大多数固定大小的数据集来说都是通用方案。不过，假如你处理的是由组织在子文件夹中的单个图像文件构成的图像数据集（比如上面的 MNIST 数据集），那么有一种更方便的数据集加载方式，我们将在下一节讨论。

## 使用 ImageFolder 创建数据集

当我们处理图像文件夹层级结构时，使用 `ImageFolder` 可以让数据集加载方便得多。让我们看看它是如何工作的。

这样一来，我们不必再定义自定义数据集（如前面的步骤 1 所示），只需用 `ImageFolder` 从文件夹层级创建数据集即可。这里，子文件夹就是类别标签：

<img src=”/images/blog/2022/datapipes/image-folder-2.jpg” width=500 =”MNIST dataset subfolders.”>

代码如下：

```python
from torchvision.datasets import ImageFolder

train_dataset = ImageFolder(
    root="mnist-pngs/train",
    transform=data_transforms["train"]
)
  
test_dataset = ImageFolder(
    root="mnist-pngs/test",
    transform=data_transforms["test"]
)
```

那验证集怎么办？我们可以使用 `random_split` 函数从训练数据集中创建一个验证子集：

```python
from torch.utils.data.dataset import random_split

train_dataset, val_dataset = random_split(
    train_dataset, 
    lengths=[55000, 5000]
)
```

然后，我们可以原封不动地复用上面步骤 3 和步骤 4 的代码。

完整示例请参见 [`2_imagefolder.py`](https://github.com/rasbt/datapipes-blog/blob/main/1_dataset-csv.py) 文件。

**这种方法的一个潜在缺点**

在转向 DataPipes 之前，你能看出这种方法的一个缺点吗？与我们自定义 Dataset 的做法相比，上面的 `ImageFolder` 方法不允许我们为验证集指定自定义的变换方法。我们最终只能使用训练集的变换（包括随机数据增强）。这虽然不是世界末日，但也不理想。（在实践中，为了绕开这个问题，我们可以单独创建一个验证集文件夹。）

## DataPipes 入门

既然我们已经理解了 Dataset 和 DataLoader 如何（协同）工作，接下来进入有趣的部分——新的 DataPipes。

随着 PyTorch 1.11 的发布，PyTorch 团队[宣布](https://pytorch.org/blog/pytorch-1.11-released/)了 [TorchData](https://github.com/pytorch/data) 的 beta 版本。TorchData 是一个 Python 库，包含面向 PyTorch 的新数据加载工具。简而言之，TorchData 围绕所谓的数据管道（data pipes）和可复用数据组件展开。

TorchData 团队的目标是最终取代 Dataset 和 DataLoader 两个类。为什么？因为有时为不同的用例创建自定义 Dataset 会很繁琐。用一组经过充分优化的组件来构建 Dataset 或许更高效。此外，DataLoader 的功能过于臃肿，DataPipes 背后的目标之一就是把这些功能外包给 DataPipe 组件。

目前，DataPipe 与现有的 DataLoader 兼容，可以作为 Dataset 的即插即用替代品。不过在未来，PyTorch 团队可能会专门为 DataPipes 开发一个更精简的 [DataLoader2](https://github.com/pytorch/data/blob/main/torchdata/dataloader2/dataloader2.py#L46)。

下图展示了 DataPipes 与 DataLoader 之间的关系：

![Datapipes datapipe dropin](https://sebastianraschka.com/images/blog/2022/datapipes/datapipe-dropin.webp)

再强调一次，关键思路是：我们可以通过串联单个 DataPipe 组件来构建每个 DataPipe（训练数据管道、验证数据管道和测试数据管道）。接下来小节中的代码示例会把这一点讲得更清楚。

### 类构造器与函数式形式

大多数 DataPipe 既可以通过类构造器使用，也可以通过 PyTorch 团队推荐的函数式形式使用。函数式形式本质上就是方法调用。例如下面这个例子：我们先用类构造器实例化一个用于打开文件的新数据管道，然后用 CSVParser 类构造器为它串联上一个 CSV 解析器：

```python
new_dp = dp.iter.FileOpener([csv_file])
new_dp = dp.iter.CSVParser(new_dp, skip_lines=1)
# returns tuples like ('train/0/16585.png', '0')
```

函数式形式（PyTorch 团队推荐的方式）如下所示：

```python
new_dp = dp.iter.FileOpener([csv_file])
new_dp = new_dp.parse_csv(skip_lines=1)
# returns tuples like ('train/0/16585.png', '0')
```

### IterDataPipes 与 MapDataPipes

截至本文撰写时，DataPipes 有两种类型：[Iterable 风格 DataPipes（IterDataPipe）](https://meta-pytorch.org/data/0.3/torchdata.datapipes.iter.html)和 [Map 风格 DataPipes（https://meta-pytorch.org/data/0.3/torchdata.datapipes.map.html）](https://meta-pytorch.org/data/0.3/torchdata.datapipes.map.html)。

IterDataPipes 围绕用于取数的 `__iter()__` 协议构建。它常用于按顺序（而非随机顺序）访问数据的操作。一个常见用例是处理数据流。IterDataPipes 的另一个例子是 FileOpener，它根据文件路径列表打开文件。我建议浏览一下 [IterDataPipes 列表](https://meta-pytorch.org/data/0.3/torchdata.datapipes.iter.html)，大致了解现有的 IterDataPipes 类型。

MapDataPipes 则围绕我们已经从 DataSet 类了解的 `__getitem__()` 和 `__len__()` 协议构建。它们更适合那种基于数据集长度、通过数据集索引进行随机访问的操作。同样，我建议你浏览一下 [map 风格 DataPipes](https://meta-pytorch.org/data/0.3/torchdata.datapipes.map.html) 的列表，看看已有哪些类型的 MapDataPipes。

注意，对于打乱（shuffling）这类功能，同时存在 IterDataPipe 版的 `Shuffler` 和 MapDataPipe 版的 `Shuffler`。迭代式的 Shuffler 在缓冲区上操作（因此只在一个窗口大小内打乱），而 map 风格的 Shuffler 没有这个限制，会考虑整个数据集来打乱。

IterDataPipe 的打乱如下所示，其中必须指定缓冲区大小：

```python
new_dp = dp.iter.FileOpener([csv_file])
...
new_dp = new_dp.shuffle(buffer_size=10,000)
new_dp = new_dp.map(open_image)
...
```

（没错，IterDataPipes 也有 `.map` 方法 🤯。）

不过，我们可以用 `.to_map_datapipe()` 把 IterDataPipe 转换为 MapDataPipe，从而进行全局打乱：

```python
new_dp = dp.iter.FileOpener([csv_file])
...
new_dp = new_dp.to_map_datapipe().shuffle(indices=np.arange(len))
new_dp = new_dp.map(open_image)
```

下一节中，我们将为 MNIST 数据集实现 DataPipe 方案，讨论它在实践中如何运作。

## 用于图像与 CSV 数据集的 DataPipes

现在我们已经熟悉了 DataPipes 的整体概念，接下来复现 [Dataset 与 DataLoader] 一节中处理包含 MNIST 图像文件路径的 CSV 文件的做法。

我们将构建三个 DataPipe：分别用于训练、验证和测试。所以，先实现一个创建数据管道的便捷函数，以避免重复代码：

```python
def build_data_pipe(csv_file, transform, len=1000, batch_size=32):
    new_dp = dp.iter.FileOpener([csv_file])

    new_dp = new_dp.parse_csv(skip_lines=1)
    # returns tuples like ('train/0/16585.png', '0')

    new_dp = new_dp.map(create_path_label_pair)
    # returns tuples like ('mnist-pngs/train/0/16585.png', 0)
    
    if transform == "train":
        new_dp = new_dp.shuffle(buffer_size=len)

    new_dp = new_dp.sharding_filter()
    # important to use sharding_filter after (not before) shuffling

    new_dp = new_dp.map(open_image)

    if transform == "train":
        new_dp = new_dp.map(apply_train_transforms)
        new_dp = new_dp.batch(batch_size=batch_size, drop_last=True)

    elif transform == "test":
        new_dp = new_dp.map(apply_test_transforms)
        new_dp = new_dp.batch(batch_size=batch_size, drop_last=False)

    else:
        raise ValueError("Invalid transform argument.")

    new_dp = new_dp.map(default_collate)
    return new_dp
```

在上面的代码中，你可以看到 DataPipes 串联特性的实际运作。我们从一个文件打开器 IterDataPipe 开始，然后使用前面讨论的函数式形式为其添加若干组件。

你可能还注意到有一些尚未定义的变量：`create_path_label_pair`、`open image`、`apply_train_transforms` 、 `apply_test_transforms` 和 `default_collate`。这些是我们配合 `.map()` 使用的函数，下面就来定义它们：

```python
def create_path_label_pair(inputs):
    img_path, label = inputs
    img_path = os.path.join(IMG_ROOT, img_path)
    label = int(label)
    return img_path, label

def open_image(inputs):
    img_path, label = inputs
    img = Image.open(img_path)
    return img, label

def apply_train_transforms(inputs):
    x, y = inputs
    return DATA_TRANSFORMS["train"](x), y

def apply_test_transforms(inputs):
    x, y = inputs
    return DATA_TRANSFORMS["test"](x), y
```

（`DATA_TRANSFORMS` 是一个用全局变量做的变通，因为 `.map()` 目前无法接收额外参数。建议查看完整的 [3_datapipes-csv.py](https://github.com/rasbt/datapipes-blog/blob/main/3_datapipes-csv.py) 文件以了解上下文。）

现在，使用我们的 `build_data_pipe` 工具函数，就可以构建三个 DataPipe 了：

```python
train_dp = build_data_pipe(
    csv_file="mnist-pngs/new_train.csv", transform="train", len=45000, batch_size=32
)

val_dp = build_data_pipe(
    csv_file="mnist-pngs/new_val.csv", transform="test", batch_size=32
)

test_dp = build_data_pipe(
    csv_file="mnist-pngs/test.csv", transform="test", batch_size=32
)
```

注意，这个数据集相对较小，所以我们可以用整个训练集的长度来打乱。另外请注意，打乱和 `batch_size` 现在都定义在 DataPipe 内部，而不是 `DataLoader` 内部。这是能为未来开发更简洁的 [DataLoader2](https://github.com/pytorch/data/blob/main/torchdata/dataloader2/dataloader2.py#L46) 创造条件的诸多变化之一。

DataPipe 定义好之后，我们就可以在 DataLoader 中把它们当作 Dataset 的即插即用替代品：

```python
from torch.utils.data.backward_compatibility import worker_init_fn

train_loader = DataLoader(
    dataset=train_dp, shuffle=True, num_workers=2, worker_init_fn)

val_loader = DataLoader(
    dataset=val_dp, shuffle=False, num_workers=2, worker_init_fn)

test_loader = DataLoader(
    dataset=test_dp, shuffle=False, num_workers=2, worker_init_fn)
```

（如果你对 DataLoader 中的 `worker_init_fn` 和打乱参数感到好奇，请继续关注下文的[已知注意事项](#KnownCaveats)一节。）

现在，和之前一样，我们可以用下面的代码试一试我们的数据加载管道：

```python
    num_epochs = 1
    for epoch in range(num_epochs):

        for batch_idx, (x, y) in enumerate(train_loader):
            if batch_idx >= 3:
                break

            # collate added an extra dimension
            x, y = x[0], y[0]
            print(" Batch index:", batch_idx, end="")
            print(" | Batch size:", y.shape[0], end="")
            print(" | x shape:", x.shape, end="")
            print(" | y shape:", y.shape)

    print("Labels from current batch:", y)
```

如果一切正常，应该会打印出以下内容：

```python
 Batch index: 0 | Batch size: 32 | x shape: torch.Size([32, 1, 28, 28]) | y shape: torch.Size([32])
 Batch index: 1 | Batch size: 32 | x shape: torch.Size([32, 1, 28, 28]) | y shape: torch.Size([32])
 Batch index: 2 | Batch size: 32 | x shape: torch.Size([32, 1, 28, 28]) | y shape: torch.Size([32])
Labels from current batch: tensor([[1, 1, 7, 8, 3, 6, 6, 5, 1, 2, 4, 9, 4, 5, 1, 5, 1, 9, 4, 0, 4, 5, 1, 9,
         6, 8, 0, 0, 9, 0, 5, 4]])
```

### 已知注意事项

**多进程**

目前有几个值得提及的注意事项（感谢 [Nicolas Hug](http://nicolas-hug.com) 指出这些问题）。

首先，注意我们在前面的 `build_data_pipe` 函数中使用了一个 [ShardingFilter](https://meta-pytorch.org/data/0.3/generated/torchdata.datapipes.iter.ShardingFilter.html)：

```python
...
new_dp = new_dp.sharding_filter()
...
```

截至本文撰写时，这是在使用多于 1 个 worker 时避免数据重复的必要变通手段。例如，看下面这个迭代 0-4 范围内数字的例子：

**输入：**

```python
from torchdata.datapipes.iter import IterableWrapper

dp = IterableWrapper(range(5))
list(DataLoader(dp, num_workers=1))
```

**输出：**

```python
[tensor([0]),
 tensor([1]),
 tensor([2]),
 tensor([3]),
 tensor([4])]
```

在上面的代码示例中，输出符合预期。但注意，如果换成 2 个 worker，就会出现数据重复问题：

**输入：**

```python
list(DataLoader(dp, num_workers=2))
```

**输出：**

```python
[tensor([0]),
 tensor([0]),
 tensor([1]),
 tensor([1]),
 tensor([2]),
 tensor([2]),
 tensor([3]),
 tensor([3]),
 tensor([4]),
 tensor([4])]
```

为了避免这个问题，我们可以用 `.sharding_filter` 作为变通手段，配合一个向后兼容的 worker 初始化函数（`work_init_fn`）：

**输入：**

```python
from torch.utils.data.backward_compatibility import worker_init_fn

dp = IterableWrapper(range(5))
dp = dp.sharding_filter()
list(DataLoader(dp, num_workers=2, worker_init_fn=worker_init_fn))
```

**输出：**

```python
[tensor([0]),
 tensor([1]),
 tensor([2]),
 tensor([3]),
 tensor([4])]
```

**打乱**

另外，注意即使我们在数据管道中加入了打乱操作，数据默认也不会被打乱：

**输入：**

```python
dp = IterableWrapper(range(5))
dp = dp.shuffle()
dp = dp.sharding_filter()
list(DataLoader(dp, num_workers=2, worker_init_fn=worker_init_fn))
```

**输出：**

```python
[tensor([0]),
 tensor([1]),
 tensor([2]),
 tensor([3]),
 tensor([4])]
```

重要的是把 sharding filter 放在打乱操作之后，以确保数据被正确打乱。

为了在 PyTorch 1.11 中实现打乱，我们还必须在 DataLoader 中也启用打乱：

**输入：**

```python
list(DataLoader(
    dp, num_workers=2, worker_init_fn=worker_init_fn, shuffle=True))
```

**输出：**

```python
 tensor([2]),
 tensor([4]),
 tensor([0]),
 tensor([3]),
 tensor([2])]
```

（注意，目前有一个小 bug，数字可能会重复，如上所示。目前避免这个问题的一种办法是只用 1 个 worker。）

有人可能会说，打乱是 DataLoader 完成的，而不是 DataPipe 的 `.shuffle`。我们可以在一个没有 shuffler 的 DataPipe 上运行下面的代码，来确认打乱确实是由 DataPipe 完成的：

**输入：**

```python
dp = IterableWrapper(range(5))
dp = dp.sharding_filter()
list(DataLoader(
    dp, num_workers=2, worker_init_fn=worker_init_fn, shuffle=True))
```

**输出：**

```python
[tensor([0]),
 tensor([1]),
 tensor([2]),
 tensor([3]),
 tensor([4])]
```

换句话说，当我们用 DataPipe 而不是 Dataset 作为 DataLoader 的输入时，DataLoader 的 `shuffle` 参数就变成了 DataPipe shuffler 的开关。

这一行为最近在 PyTorch 的 nightly 发布版中得到了处理：把 DataLoader 中 `shuffle` 参数的默认值从 `False` 改为 `None`，这样只要 DataPipe 包含 shuffler，打乱默认总是启用。

## 结论

本文介绍了 Dataset、DataLoader 和 DataPipes。TorchData 引入的新 DataPipe 类旨在作为传统 Dataset 类的可组合、即插即用替代品。看过这些示例之后，你可能有许多疑问！

### 哪个更方便？

就我个人而言，对于与本文 MNIST 示例结构类似的图像数据集，我觉得 Dataset 比 DataPipes 更方便。（而且 ImageFolder 的便利性很难被超越，只除了我们讨论过的训练变换缺陷。）不过，这可能是因为我对 DataPipes 还不熟，还需要时间适应。但我可以预见，对于其他用例，尤其是处理流式数据等场景，DataPipes 可能具有某些优势。此外还有许多[现成的 IterDataPipes](https://meta-pytorch.org/data/0.3/torchdata.datapipes.iter.html)和 [MapDataPipes](https://meta-pytorch.org/data/0.3/torchdata.datapipes.map.html)可供复用，这很不错。

### 哪个性能更好？

根据我的快速测试，我没有察觉到任何性能差异。说实话，我也没指望有。在本文构建的 DataPipes 中，我们仍然使用同样的函数来打开图像和做数据变换。唯一的区别是现在可以串联这些操作。不过 DataPipes 的好处在于，它让开发与共享变得更容易，这能为开发更高性能的管道铺路。

### 该用哪个？

目前很难说该推荐哪一个。对于标准任务，比如本文中的图像数据集示例，眼下继续用 Dataset 和 DataLoader 应该没问题。不过从长远来看，开始采用 DataPipes 也许并无坏处，因为它们可能会成为 PyTorch 中主流的数据加载方式。而且，熟悉它之后，需要时你可以更容易地为更特殊的场景和文件格式构建专用的数据管道。

---

另外请记住，DataPipes 仍处于 beta 阶段。如果你当前使用 PyTorch 1.11 并想使用 DataPipes，我建议安装 PyTorch nightly 版本，以在 PyTorch 1.12 发布之前获得最新的更新和修复。你可以通过 `pip` 升级到最新的 nightly 版本（具体命令参见 PyTorch 官网上的[安装菜单](https://pytorch.org)）。
