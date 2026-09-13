---
title: "深度学习模型服务化：Lightning + 云"
title_en: "DL Model Serving: Lightning + Cloud"
source: https://sebastianraschka.com/blog/2022/lightning-app-srgan-2.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 深度学习模型服务化：Lightning + 云

> 原文：[DL Model Serving: Lightning + Cloud](https://sebastianraschka.com/blog/2022/lightning-app-srgan-2.html)

在本文中，我们将使用 [Lightning 框架](https://lightning.ai)把一个超分辨率应用部署到云上。这里的首要目标是看看创建并分享一个研究 demo 有多么容易。不过，云的用途可不只是模型*分享*：我们还将学习如何利用额外的 GPU 资源进行模型*训练*。

---

- [分享你的研究](#SharingYourResearch)
- [Lightning 应用回顾](#LightningAppRecap)
- [在云上运行研究 demo](#RunningaResearchDemoontheCloud)
- [配置云端：选择文件与资源](#ConfiguringtheCloud:ChoosingFilesandResources)
  - [需要哪些配置？](#WhatAretheSetupRequirements)
  - [通过 CloudCompute 选择硬件](#ChoosingHardwareviaCloudCompute)
- [在云上训练模型](#TrainingaModelontheCloud)
  - [一个简单的 Python 脚本组件](#ASimplePythonScriptComponent)
  - [保存与下载文件输出](#SavingandDownloadingFileOutputs)
  - [理解 Lightning 存储](#UnderstandingLightningStorage)
  - [创建一个训练并保存的应用](#CreatingaTrainSaveApp)
- [加分项：一个更完善的 PyTorch Lightning 训练应用](#Bonus:AMoreSophisticatedPyTorchLightningTrainingApp)
- [下一篇：开发自定义组件](#Next:DevelopingCustomComponents)

## 分享你的研究

我至今还记得当初作为研究生开始科研生涯时的兴奋。那正是 GitHub 刚刚作为一个分享代码的新平台崭露头角的时候。那真是太棒了，为代码分享与协作打开了如此多的机会。

幸运的是，在过去几年里，越来越多的人开始在发表论文的同时共享代码。而且，许多研究者现在还会随实验流水线一起提供易用的 Python 脚本或 Jupyter notebook。

不过，现在已经是 2022 年了，虽然我认为 GitHub 仍然是共享研究代码的主要方式，但也该为我们的研究添加一个新的维度，让它脱颖而出：可以与他人分享的交互式应用。多年以前，[我写过一章关于如何用 Flask 做这件事的内容](https://github.com/rasbt/python-machine-learning-book/tree/master/code/ch09)，但那种方式已经过时，而且除了简单的研究 demo 之外很难扩展。再说，谁有时间去折腾基础设施呢？

那么，让我们把在[第 1 部分](https://sebastianraschka.com/blog/2022/lightning-app-srgan-1.html)中开发的超分辨率应用拿到云上去运行吧。

## Lightning 应用回顾

在[第 1 部分](https://sebastianraschka.com/blog/2022/lightning-app-srgan-1.html)中，我们在本地创建并运行了第一个 Lightning 应用。这主要是为了练习、理解核心 API：`LightningApp`、`LightningFlow` 和 `LightningWork`。如果你不想重读[第 1 部分](https://sebastianraschka.com/blog/2022/lightning-app-srgan-1.html)，我完全理解。下面是对主要思想的简要总结。（如果你对第 1 部分已经很熟悉，可以直接跳到下一节。）

Lightning 应用由一个主 LightningFlow（根 Flow）构成，它负责编排 LightningWork 和其他 LightningFlow（子 Flow）组件。Flow 用于编排，而 Work 通常用于干重活——也就是任何耗时超过零点几秒的实质性计算。除了有一个根 Flow 之外，我们可以按任意喜欢的方式组织组件树。唯一的限制是 Work 组件必须作为终端节点，如下图所示：

![Lightning app srgan 2 app component](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-2/app-component.webp)

值得强调的是，这个组件树是一个动态的、响应式的系统，而不是有向无环图（DAG)。这意味着各个 Work 可以独立运行，通信则通过由 Flow 编排的状态变更来进行。如果你以前用过 [React](https://reactjs.org)，可以把它类比为一种相关的思路。长话短说，Lightning 应用的组件树让我们能够构建非常灵活的机器学习系统。

组件树基于 Flow 和 Work，而 `LightningApp` 则会反复调用根 Flow 的 run 方法，由后者编排各个 Work 组件，如下图所示：

![Lightning app srgan 2 app flow work](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-2/app-flow-work.webp)

在内部，组件树中的通信通过状态变更实现。每个 Work 都有自己的状态，可以并行运行，并能立即对其他 Work 作出响应。更深入的讨论可以观看 Luca Antiga 关于 Lightning 内部机制的[演讲](https://www.youtube.com/watch?v=58qpOxKRzqY&t=3964s)。

值得强调的关键点是：Work 组件可以独立运行。这让我们可以把不同的 Work 组件放到不同的硬件上。如果我们用 Lightning 框架搭建一个从训练到部署的机器学习生产系统，这一点会非常有用。**例如，我们可以用一个强大的多节点云端 GPU 集群通过一个 Work 组件来训练模型，然后用一台更便宜的机器通过另一个 Work 组件进行推理。**正如我们将在下一节看到的，为不同的 Work 组件使用不同的硬件非常简单，只需要 1 行代码！

## 在云上运行研究 demo

在第 1 部分中，我们通过以下命令在本地运行了[我们的 Lightning 应用](https://github.com/rasbt/srgan-lightning-blog/tree/main/part1-code/superres-local)：

```python
lightning run app app.py
```

在本地运行应用对调试等场景很有用。但如果我们想使用额外的硬件资源，或者通过互联网与他人分享我们的应用呢？只需加上 `--cloud` 参数，就可以在云上运行同一个应用：

```python
lightning run app app.py --cloud
```

![Lightning app srgan 2 cloud fast](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-2/cloud-fast.gif)

（你可以在 GitHub 上的[这里](https://github.com/rasbt/srgan-lightning-blog/tree/main/part2-code/superres-from-part1)找到这个应用的源代码。并且可以在[这里](https://01g66tfn2df2jy0q2dmmkj8wpg.litng-ai-03.litng.ai/view/SRGAN%20Demo)体验这个应用的云端交互版本。）

现在，如果我们想给应用起一个更有创意的名字，可以通过 `--name` 选择自定义名称：

```python
lightning run app app.py --cloud --name superres-demo-1
```

这非常简单，对吧？严格来说，既然我们已经成功在云上运行了这个应用，文章到这里就可以结束了……

不过我猜你肯定有很多问题，比如

- 需要编写 setup 或 config 文件吗？
- 这是免费的吗？
- 它使用了哪些计算资源？
- 能带上我们自己的集群吗？

所以，在接下来的几节中，让我们更深入地探讨这些问题。

## 配置云端：选择文件与资源

当我们在上一节使用 `--cloud` 参数时，发生了两件事：

1. 我们的应用被自动上传到了 Lightning Cloud；
2. 它使用了一个免费的[默认 CPU 云实例](https://lightning.ai/lightning-docs/core_api/lightning_work/compute.html?highlight=cloudcompute)。

本节将揭开幕后机制，讨论配置要求以及如何选择不同的计算资源。

### 需要哪些配置？

正如你在上面看到的，当我们执行以下命令时，在云上运行应用并不需要任何特殊的配置流程：

```python
lightning run app app.py --cloud
```

（好吧，除了 Lightning 会在你尚未登录时提示你登录。）

Lightning 是如何知道该如何配置我们的计算实例来运行代码的呢？同样，这一切都是自动完成的；我们唯一需要的是一个与 pip 兼容的 `requirements.txt` 文件放在应用文件夹中。不过，为了可复现性，我们通常本来就会创建一个 `requirements.txt`：

![Lightning app srgan 2 requirements](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-2/requirements.webp)

实际上，如果你运行

```python
lightning run app app.py --cloud
```

Lightning 会上传当前目录中的所有文件。要排除特定文件，我们可以创建一个 `.lightningignore` 文件，它的作用与 `.gitignore` 类似。

（另外，第一次使用 `run` 命令时，Lightning 会创建一个 `.lightning` 配置文件——只有当我们想修改应用名称时才需要编辑它。）

### 通过 CloudCompute 选择硬件

当我们在上一节使用 `--cloud` 参数时，我们的应用使用的是免费的[默认 CPU 云实例](https://lightning.ai/lightning-docs/core_api/lightning_work/compute.html?highlight=cloudcompute)。不过，有时我们希望使用更强大的硬件，例如用于模型训练的多 GPU 集群。那么，让我们看看这是如何做到的。

前面我们了解到，各个 LightningWork 彼此独立运行。这很好，因为它允许我们选择不同的、相互独立的计算资源。例如，我们可以为一个负责训练模型的 Work 组件使用一台配备多 GPU 的强大云实例。不过，这样的云实例用于推理就大材小用了。所以，我们可以在训练完成后用更便宜的 CPU 或 GPU 来提供模型服务。

那么如何选择云资源呢？我们可以像下面这样为 LightningWork 组件提供一个额外的 `cloud_compute=L.CloudCompute(...)` 参数：

```python
class RootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()

        self.train_model = MyTrainingWork(
            ..., 
            cloud_compute=L.CloudCompute("gpu-fast-multi", idle_timeout=20)
        )
        self.serve_model = MyServingWork(
            ...,
            cloud_compute=L.CloudCompute("cpu-medium")
        )

    def run(self):
        self.train_model.run()
        self.serve_model.run()
```

（截至撰写本文时，`"gpu-fast-multi"` 对应 4xV100 GPU。当前支持的实例类型列表可以在[这里](https://lightning.ai/lightning-docs/core_api/lightning_work/compute.html?highlight=cloudcompute)找到。）

注意，上面代码中的 `idle_timeout=20` 参数是可选的；它确保 GPU 实例会在训练结束、不再需要之后的 20 秒自动关闭。这样我们就不会在不必要时浪费云端额度去运行一个 4xV100 GPU 集群。

---

**BYOC**

默认情况下，使用 `--cloud` 标志会使用 Lightning Cloud 的资源。不过，也可以 BYOC（BYOC 是 "bring your own cluster" 的缩写——没错，这是笔者最近在工业界学到的一个流行技术行话）。请注意，截至撰写本文时，此功能仅可按需申请使用。

---

## 在云上训练模型

我们这个简单的超分辨率研究 demo 使用了一个预训练模型，而我们也刚刚学会了如何把它分享给世界。不过，正如前面提到的，我们也可以把云用于模型训练。事实上，Lightning 可能最常见的用例就是构建*训练与部署*（Train & Deploy）应用。

在本节中，让我们采用自底向上的方式在云上训练一个模型。由于 Lightning 应用就是普通的 Python 代码，我们本可以把训练代码放进某个 Work 的 run 方法里。不过，现有的组件中已经有一个 Work 组件可以让你运行任意的 Python 脚本。让我们构建一个在单 GPU 上训练 PyTorch 模型的最小应用，看看它是如何工作的。

### 一个简单的 Python 脚本组件

在本节中，我们将在 PyTorch 中使用云端 GPU 训练一个深度神经网络。不过，这个 PyTorch 训练脚本实际上只是任何你想运行的任意脚本的一个占位符。

你可以在 GitHub 上的[这里](https://github.com/rasbt/srgan-lightning-blog/tree/main/part2-code/train)找到这个应用的完整代码。它由 3 个主要文件组成

- [`my_train_script.py`](https://github.com/rasbt/srgan-lightning-blog/blob/main/part2-code/train/my_train_script.py)：一个任意的 PyTorch 脚本（这里是：在 MNIST 上训练的多层感知机。）
- [`app.py`](https://github.com/rasbt/srgan-lightning-blog/blob/main/part2-code/train/app.py)：Lightning 应用代码。
- [`requirements.txt`](https://github.com/rasbt/srgan-lightning-blog/blob/main/part2-code/train/requirements.txt)：`pip` 所需的包版本。

![Lightning app srgan 2 train app](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-2/train-app.webp)

对于这个应用，我们不使用任何 UI。这个应用的全部目标只是使用云端 GPU 执行一个任意的 Python 脚本。这个极简应用的代码如下：

```python
import lightning as L
from lightning.app.components.python import TracerPythonScript

class RootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()

        self.train_model = TracerPythonScript(
            script_path="my_train_script.py",
            script_args=["--num_epochs=1"],
            cloud_compute=L.CloudCompute("gpu", idle_timeout=60),
        )

    def run(self):
        self.train_model.run()

app = L.LightningApp(RootFlow())
```

观察上面的代码，可以看到我们的组件树由一个 LightningFlow 和一个 LightningWork 组成。这里我们使用了 [`TracerPythonScript`](https://lightning.ai/lightning-docs/api_reference/generated/lightning_app.components.python.tracer.TracerPythonScript.html?highlight=tracerpythonscript)，它是一个用于运行 Python 脚本（可带命令行参数）的 LightningWork 组件。在我们的例子里，我们把 [`my_train_script.py`](https://github.com/rasbt/srgan-lightning-blog/blob/main/part2-code/train/my_train_script.py) 文件配置成通过 Python 标准库 [`argparse`](https://docs.python.org/3/library/argparse.html) 接受命令行参数。

此外，我们使用 `CloudCompute` 来指定 GPU 资源。截至撰写本文时，`L.CloudCompute("gpu")` 使用的是一块价格实惠的 T4 GPU，每小时成本约 50 美分。（所有受支持的 GPU 实例类型的列表可以在[这里](https://lightning.ai/lightning-docs/core_api/lightning_work/compute.html#customize-my-work-resources)找到。）

与前面几节类似，我们可以通过如下命令运行这个应用：

```python
lightning run app app.py --cloud
```

运行上述代码应该会在新的浏览器窗口中打开这个应用。模型开始训练可能需要片刻时间，但你应当能在 Lightning 控制台中看到训练输出。另外，由于我们指定了 `idle_timeout=60`，应用会在完成训练一分钟后关闭 GPU 实例。

![Lightning app srgan 2 train app results](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-2/train-app-results.webp)

### 保存与下载文件输出

在上一节中，我们运行了一个简单的"训练"应用，它在 Lightning Cloud 上运行了一个 Python 脚本 `my_python_script.py`。这是一个非常简单的应用，把一个深度神经网络的损失和预测准确率打印到命令行：

```python
Epoch: 001/001 | Batch: 000/234 | Loss: 2.3135
Epoch: 001/001 | Batch: 050/234 | Loss: 0.4393
Epoch: 001/001 | Batch: 100/234 | Loss: 0.2753
Epoch: 001/001 | Batch: 150/234 | Loss: 0.2312
Epoch: 001/001 | Batch: 200/234 | Loss: 0.2797
Total Training Time: 0.03 min
Training accuracy: 94.03%
Test accuracy: 93.80%
```

在真实场景中，我们可能会希望保存模型权重——除非我们只是在做超参数优化，否则如果训练好的模型以后用不上，在云上训练它又有什么意义呢？所以，让我们简要看看 Lightning 是如何管理文件的。

### 理解 Lightning 存储

回到我们之前关于 LightningWork 的观点：让各个 LightningWork 独立运行的一个令人愉快的副作用是，我们可以把它们放在完全不同的机器上。例如，我们可以租用昂贵的 GPU 集群做模型训练，再用一台更便宜的计算机做推理。然而，随之而来的结果是，各个 LightningWork 也拥有各自独立的文件系统。

那么我们如何在 Work 之间共享文件呢？主要有两个存储 API：

- `Drive`：你可以把 Lightning 的 [Drive](https://lightning.ai/lightning-docs/glossary/storage/drive.html) 对象想象成一个可以放置文件的虚拟位置——类似于 Google Drive、OneDrive 或 Dropbox。它是任何 LightningWork 都能访问的位置。
- `Path`：Lightning 的 [Path](https://lightning.ai/lightning-docs/glossary/storage/path.html) 对象比 Drive 更具方向性或针对性。Path 只能沿一个方向在 LightningWork 之间传递：从文件创建者 Work 组件传给文件接收者 Work 组件。

什么时候用哪个？虽然 Drive（作为中心位置）和 Path（用于单向文件传输）略有不同，但通常二者用哪个都行——归根结底主要看个人偏好。关于二者差异的更多信息可以在[这里](https://lightning.ai/lightning-docs/glossary/storage/differences.html)阅读。

### 创建一个训练并保存的应用

好了，在对 Lightning 的 Path 与 Drive 存储 API 做了概念层面的简介之后，让我们看看在实践中如何使用它们。在本节中，我们将升级"训练"应用，以便从云上下载训练好的模型。要做到这一点，我们必须把本地文件添加到 Lightning 文件系统中，以便随后从 Web UI 访问并下载它们。这里的*本地*文件指的是运行 LightningWork 的云实例所创建的文件。

首先，我们将修改[我们的 PyTorch 模型训练脚本](https://github.com/rasbt/srgan-lightning-blog/blob/main/part2-code/train-and-save/my_train_script.py)，让它保存模型权重并写出一个日志文件。

我们添加几个 argparse 选项，以便通过命令行参数定义输出文件名，如下所示：

```python
python my_train_script.py \
--num_epochs 1 \
--model_out my_trained_model.pt \
--log_out log.txt
```

你可以把它看作我们在研究项目中通常会写的通用模型训练 Python 脚本。

现在，让我们看一下 [`app_with_path.py`](https://github.com/rasbt/srgan-lightning-blog/blob/main/part2-code/train-and-save/app_with_path.py) 文件，它是前一个 [app.py](https://github.com/rasbt/srgan-lightning-blog/blob/main/part2-code/train/app.py) 文件的修改版：

```python
import shutil
from pathlib import Path

import lightning as L
from lightning.app.components.python import TracerPythonScript

class TrainAndSaveModel(TracerPythonScript):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create virtual paths
        self.model_path = "lit://my_trained_model.pt"
        self.log_path = "lit://log.txt"

    def on_after_run(self, _):
        # copy files from local file system to the virtual paths
        shutil.copy(Path.cwd() / "my_trained_model.pt", self.model_path)
        shutil.copy(Path.cwd() / "log.txt", self.log_path)

class RootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()

        self.train_model = TrainAndSaveModel(
            script_path="my_train_script.py",
            script_args=[
                "--num_epochs=1",
                "--model_out=my_trained_model.pt",
                "--log_out=log.txt",
            ],
            cloud_compute=L.CloudCompute("gpu", idle_timeout=60),
        )

    def run(self):
        self.train_model.run()

app = L.LightningApp(RootFlow())
```

这个应用乍看之下可能非常复杂，所以让我们一步一步来梳理。

`RootFlow` 几乎没有变化。与之前的训练版 [`app.py`](https://github.com/rasbt/srgan-lightning-blog/blob/main/part2-code/train/app.py) 文件相比，第一个区别是 `my_train_script.py` 现在接受多个命令行参数。第二个区别是我们现在使用 `TrainAndSaveModel` 而不是 `TracerPythonScript`。这里的 `TrainAndSaveModel` 是我们通过继承 `TracerPythonScript` 创建的自定义组件。

让我们更仔细地看看自定义的 `TrainAndSaveModel` Python 类。我们让它继承自 `TracerPythonScript`，但做了两处小修改。第一，在构造函数中，我们创建了两个虚拟路径：

```python
# create virtual paths
self.model_path = "lit://my_trained_model.pt"
self.log_path = "lit://log.txt"
```

第二，我们定义了一个自定义的 `.on_after_run()` 方法：

```python
def on_after_run(self, _):
    # copy files from local file system to the virtual paths
    shutil.copy(Path.cwd() / "my_trained_model.pt", self.model_path)
    shutil.copy(Path.cwd() / "log.txt", self.log_path)
```

LightningWork 组件的 `on_after_run` 方法有一个特殊行为：它会在该 Work 的 `.run()` 方法执行完毕之后被调用。在这里，`on_after_run` 方法把文件从 Work 所在机器的本地文件系统（`Path.cwd() / "my_trained_model.pt"`）复制到我们在 Lightning 存储中创建的虚拟位置（`"lit://my_trained_model.pt"`）。

就是这样。现在，我们可以像往常一样运行这个应用：

```python
lightning run app app_with_path.py --cloud
```

运行完成后，我们应该就能从 Storage UI 下载日志文件以及训练好的模型权重了：

![Lightning app srgan 2 download files](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-2/download-files.webp)

顺带一提，如果你有兴趣，这里有一个改用 Drive 而非 Path 的等价版本：[`app_with_drive.py`](https://github.com/rasbt/srgan-lightning-blog/blob/main/part2-code/train-and-save/app_with_drive.py)。（感谢 [Adrian Waelchli](https://github.com/awaelchli) 提供的所有帮助与富有洞见的讨论！）

## 加分项：一个更完善的 PyTorch Lightning 训练应用

在上一节中，我们开发了一个用于模型训练的最小应用。这主要是为了演示如何使用云端资源训练模型，以及 Lightning 存储的工作方式。

如果我们有兴趣用 Lightning 做模型训练，还有一些更完善的应用可以采用。例如，[PyTorch Lightning App](https://lightning.ai/app/WYU6CrDIAS-PyTorch%20Lightning%20App) 可以在任意 PyTorch Lightning 脚本之上叠加一个漂亮的 UI。

让我们试一试！

为此，假设我们手头有一个任意的 PyTorch Lightning 脚本。通常，我会像下面这样组织我的深度学习代码：

![Lightning app srgan 2 ptl files](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-2/ptl-files.webp)

通常，我会有一个主文件（这里是 `main.py`）来运行我的代码，并且我倾向于把数据集和模型代码分别放在独立的 Python 文件中，让项目结构更清晰。由于你可以把它当作任意的 PyTorch Lightning 代码项目，这里就不展开讨论了，但你可以在这里查看代码：[main.py](https://github.com/rasbt/srgan-lightning-blog/blob/main/part2-code/pt-lightning-app/main.py)。

现在，让我们使用来自 App Gallery 的 PyTorch Lightning App，在云上运行这段代码。

首先，让我们搭建一个全新的环境：

```python
conda create -n plapp python=3.8
conda activate plapp
pip install -r requirements.txt
```

接下来，从命令行安装 PyTorch Lightning App：

```python
# Create an App from our PyTorch Lightning script main.py
# This will create a new subfolder pl-app
lightning init pl-app main.py
```

![Lightning app srgan 2 trainer app install](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-2/trainer-app-install.webp)

在把任何东西放到云上之前，我建议先在本地试运行：

```python
# Run the App locally
lightning run app pl-app/app.py
```

![Lightning app srgan 2 ptl local](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-2/ptl-local.webp)

（注意，如果我们在本地运行，将无法选择额外的云资源等。这是因为我们输入的脚本参数取决于我们如何组织 `main.py` 文件。）
根据你的计算机性能，训练可能会非常慢。所以，我们可以通过熟悉的方式把应用放到云上运行：

```python
lightning run app pl-app/app.py --cloud
```

![Lightning app srgan 2 trainer](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-2/trainer.gif)

## 下一篇：开发自定义组件

在[第 1 部分](https://sebastianraschka.com/blog/2022/lightning-app-srgan-1.html)中，我们创建了第一个 Lightning 应用。我们从一个 Hello World 应用开始，了解幕后机制。接着，我们创建了一个简单的研究 demo，尝试了一些用户界面组件。在第 2 部分中，我们进入了有趣的部分，把应用上传到了云上。此外，我们还学习了 Lightning 存储，并看到了如何训练任意的机器学习模型。

到这里，你应该已经有足够的能力去创建（更）引人注目的研究 demo，甚至开发面向生产的*训练与部署*应用。我鼓励你去浏览 App 与 Component Gallery 寻找灵感。

不过，你很可能在寻找具有额外功能的组件。所以请期待第 3 部分，在那里我们将自定义组件（类似于本文前面我们对 `TracerPythonScript` 和 `TrainAndSaveModel` 类所做的操作）。
