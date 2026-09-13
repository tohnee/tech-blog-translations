---
title: "构建超分辨率 GAN"
title_en: "Building a Super Resolution GAN"
source: https://sebastianraschka.com/blog/2022/lightning-app-srgan-1.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 构建超分辨率 GAN

> 原文：[Building a Super Resolution GAN](https://sebastianraschka.com/blog/2022/lightning-app-srgan-1.html)

在这篇文章中，我们将构建一个 Lightning App。为什么？因为现在是 2022 年，是时候探索一种更现代的方式来交互、展示和分享我们的深度学习模型了。我们将分三个部分来解决这个问题。在这第一部分中，我们将了解什么是 Lightning App，以及如何构建一个超分辨率 GAN 演示。

![Lightning app srgan 1 srgan](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/srgan.webp)

在[第 2 部分](https://sebastianraschka.com/blog/2022/lightning-app-srgan-2.html)中，我们将把 App 部署到云端。在第 3 部分中，我们将看看如何为我们的 App 定制和开发新组件。

**作为用户，你通常不必从零构建一个 App——我们鼓励你去探索 [App Gallery](https://lightning.ai/apps)，看看是否已有现成的 App 能满足你的需求。如果你好奇 Lightning App 是如何工作的，本文将带你略窥幕后，理解其核心 API 的运作方式。**

---

- [什么是 Lightning App？](#WhatareLightningApps)
- [核心 API 的 3 个组成部分：简要概述](#The3PiecesoftheCoreAPI:ABriefOverview)
- [从一个最小化 App 开始：Hello World](#StartingwithaMinimalApp:HelloWorld)
  - [设置环境并安装 Lightning](#SettingUpYourEnvironmentandInstallingLightning)
- [开发一个最小化 App](#DevelopingaMinimalApp)
  - [LightningApp](#LightningApp)
  - [LightningFlow](#LightningFlow)
  - [LightningWork](#LightningWork)
  - [启动最小化 App](#StartingtheMinimalApp)
- [开发超分辨率 App](#DevelopingASuperResolutionApp)
  - [设置文件结构](#SettingUptheFileStructure)
  - [创建 App.py 文件](#CreatingtheApp.pyfile)
    - [RootFlow](#RootFlow)
    - [SRGAN Work 组件](#SRGANWorkComponent)
  - [About 页面前端](#TheAboutPageFrontend)
  - [运行超分辨率 App](#RunningtheSuperresolutionApp)
- [下一步：把 App 部署到云端](#Next:DeployingtheAppontheCloud)

---

## 什么是 Lightning App？

Lightning Apps 基于 2022 年 6 月 16 日刚刚发布的开源 [Lightning 框架](https://lightning.ai/lightning-docs/)。

AI 和机器学习社区已经开发了大量出色的工具和服务，从实验跟踪到各种交互式前端。Lightning AI 把不同的组件汇聚到一起，让我们能够组合和开发 Lightning App，包括那些把深度学习模型从训练带到生产的 App。简而言之，Lightning 框架让我们能够为企业和研究社区构建模块化、分布式、动态的 AI 应用。

Lightning Apps 用途非常广泛，我鼓励你去 [App Gallery](https://lightning.ai/apps) 看一看，感受一下目前已经能实现什么。不过在本文中，我们将聚焦于一个简单的场景：从零构建一个研究演示 App。因为我们总得从某处起步，而作为机器学习研究者，这能帮助我们更有效地分享和展示自己的研究。

不过，我想强调的是，Lightning Apps 并不只是研究演示；你几乎可以在 Lightning 中构建任何东西，甚至计算机集群调度器这样的东西。例如，看看 [Lightning Classroom App](https://lightning.ai/app/xJz7BU8lLO-Lightning%20Classroom)，它让我们可以在课堂教学或工作坊场景中快速启动 GPU Notebook 并分享给学生：

[![Lightning app srgan 1 classroom](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/classroom.webp)](https://lightning.ai/app/xJz7BU8lLO-Lightning%20Classroom)

此外，正如我们将在[第 2 部分](https://sebastianraschka.com/blog/2022/lightning-app-srgan-2.html)中看到的，我们可以在云端的各种 CPU 和 GPU 硬件上运行 Lightning Apps，以运行甚至训练你的模型。而最棒的一点是，你不必从零开始编写整个 App，而是可以克隆一个现有的 App——按原样使用，或根据自己的需要加以改造。

## 核心 API 的 3 个组成部分：简要概述

Lightning 框架的核心 API 由三个主要的 Python 类组成：

1. [`LightningApp`](https://lightning.ai/lightning-docs/core_api/lightning_app/)，
2. [`LightningFlow`](https://lightning.ai/lightning-docs/core_api/lightning_flow.html)，以及
3. [`LightningWork`](https://lightning.ai/lightning-docs/core_api/lightning_work/)。

LightningApp 是我们在本地或云端运行 Lightning App 的核心部分。在看看它如何工作之前，先给出一个自顶向下的概述：LightningApp 运行 LightningFlow 事件循环，而 LightningFlow 编排各个 LightningWork 组件。

当然，我们可以拥有多个 LightningWork，甚至多个 LightningFlow。但我们不要好高骛远，先从一个非常简单的 Hello World 示例开始。

## 从一个最小化 App 开始：Hello World

在本节中，我们将构建一个最小化的 Lightning App，以探索核心 API 的各个组成部分。别担心，这应该很快。而且作为小小的奖励，几分钟之后我们就会构建出第一个超分辨率 GAN 研究演示！

### 设置环境并安装 Lightning

如果你想跟着操作、在自己的电脑上尝试这些示例，我推荐几个快速的设置步骤。

作为 [conda](https://github.com/conda-forge/miniforge) 用户，为你的 App 创建一个新环境是个不错的主意（我通常对每个项目都推荐这样做——可以看看[我们关于设置 conda 环境的短课程](https://www.pytorchlightning.ai/edu#)）。

**创建新环境（可选）**

```python
conda create -n helloworldapp python=3.8
conda activate helloworldapp
```

**安装 Lightning**

你可以通过 pip 安装 Lightning：

```python
pip install -U lightning
```

或者，如果你想使用与我撰写这些代码时完全相同的包版本（Lightning 2022.6.15），可以直接从我 GitHub 上的 [requirements.txt](https://github.com/rasbt/srgan-lightning-blog/blob/main/part1-code/minimal-app/requirements.txt) 文件安装这些包：

```python
pip install -r https://raw.githubusercontent.com/rasbt/srgan-lightning-blog/main/part1-code/minimal-app/requirements.txt?token=GHSAT0AAAAAABUUA7E2554ZP6274D4K6YEYYVKI2BA
```

我还建议查看官方 [Lightning 文档](https://lightning.ai/lightning-docs/#install-lightning)以获取更多信息，以及那份 15 分钟快速入门指南——其中的 App 会训练并演示一个 PyTorch Lightning 模型：

![Lightning app srgan 1 quickstart](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/quickstart.webp)

## 开发一个最小化 App

在本节中，我们将采取自底向上的方式，从零创建一个非常简单的 Hello World App，以理解 Lightning API 的核心部分。

---

**注意**

在实践中，你通常不必从零开始构建 App。你可以前往 App Gallery，找到类似、可以克隆并修改的 App。Lightning 还有一个模板生成器，帮助你快速起步：

```python
lightning init app your-app-name
```

---

那么，让我们看看我们的最小化 Hello World App：

```python
import lightning as L

class WordComponent(L.LightningWork):
    def __init__(self, word):
        super().__init__()
        self.word = word

    def run(self):
        print(self.word)

class MyRootComponent(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.hello = WordComponent("Hello")
        self.world = WordComponent("World")
        self.counter = 0

    def run(self):
        self.counter += 1
        if self.counter <= 6:
            print("I just go with the Flow!")
        self.hello.run()
        self.world.run()

app = L.LightningApp(MyRootComponent())
```

（你可以在[这里](https://github.com/rasbt/srgan-lightning-blog/blob/main/part1-code/minimal-app/app.py)找到这个 App 的代码。）

### LightningApp

从字面意义上自底向上讨论这段代码，[LightningApp](https://lightning.ai/lightning-docs/core_api/lightning_app/lightning_app.html) 位于一个 Lightning App 的核心。它本质上是在我们的根 `LightningFlow` 组件之上运行一个无限事件循环。不过请注意，这一行

```python
app = L.LightningApp(MyRootComponent())
```

此时还没有真正运行 App。我们很快就会运行它，在那之前先简要看看代码的核心部分。

### LightningFlow

在上面的 App 中，我们定义了 `MyRootComponent`，它是一个 [LightningFlow](https://lightning.ai/lightning-docs/core_api/lightning_flow.html)。LightningFlow 是一个核心组件，负责协调一个或多个 `LightningWork` 组件（以及可选的其他 LightningFlow 子组件）。

简而言之，前述 LightningApp 以无限循环的方式执行 MyRootComponent 的 `.run()` 方法。

在这个特定的例子里，我们从一个枯燥的 `run` 方法开始，它只是在每次执行 `run` 方法时把 `counter` 属性加 `1`。在前 `6` 次调用期间，它应当打印出字符串 `"I just go with the Flow!"`。此外，还有 `self.hello.run()` 和 `self.world.run()` 这两个调用。这里的 `self.hello` 和 `self.world` 是我们在 LightningFlow 的 `__init__` 中初始化的 LightningWork 组件。LightningWork 组件是什么？很高兴你问了这个问题。

### LightningWork

[LightningWork](https://lightning.ai/lightning-docs/core_api/lightning_work/lightning_work.html) 组件让我们能够定义计算和进程，并让我们集成第三方服务。基本上，任何需要干重活的东西我们都用它。

与 LightningFlow 类似，LightningWork 组件也有一个 `run` 方法。LightningWork 作为独立进程运行，由 LightningFlow 编排。要启动一个 LightningWork 进程，我们在 LightningFlow 中初始化该 LightningWork 组件，然后在 LightningFlow 中调用它们各自的 `run` 方法（下面是前述代码的标注截图）：

![Lightning app srgan 1 annotated work](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/annotated-work.webp)

（注意，我们不仅可以从 LightningFlow 内部调用 LightningWork，还可以让多个 LightningFlow 形成层级结构，如[这里](https://lightning.ai/lightning-docs/glossary/app_tree.html)的 App 组件树可视化所示。）

### 启动最小化 App

现在，为了看看这一切是如何工作的，让我们看看启动 App 时会发生什么。如果你把上面的代码放进一个名为 `app.py` 的文件，我们可以从终端这样启动它：

```python
lightning run app app.py
```

执行上面的代码应该会在你的浏览器中打开一个新窗口。注意，对于这个 App，浏览器里还没有任何事情发生——我们稍后会讲到。不过我们可以在终端中看到如下代码输出：

![Lightning app srgan 1 run app1](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/run-app1.gif)

我敢打赌，这个输出和你预期的不一样。那么，发生了什么？

首先，为什么"I just go with the Flow"的全部六次迭代都打印在"Hello"和"World"之前？这是因为 `LightningFlow` 的 `for` 循环运行得非常非常快。或者换句话说，为各个 worker 启动独立运行进程存在一点开销，主循环能够在我们看到"hello"之前打印出全部六条"I just go with the flow"语句。（感谢 [Josh Starmer](https://www.linkedin.com/in/joshua-starmer-phd/?trk=public_post-text) 提出澄清性问题并提供反馈！）

其次，为什么 hello 和 world 都只打印了一次？`LightningFlow` 在其 run 方法内运行一个非常快的无限循环。然而，LightningWork 组件（WordComponent）默认只会被执行**一次**。

![Lightning app srgan 1 flow loop](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/flow-loop.webp)

这很有用，例如，如果我们实现一个带有模型训练组件的 App（我们只想训练一次），然后再用另一个组件部署它。不过，在某些情况下，我们想要覆盖这种行为，我们可以像下面这样修改组件来实现：

```python
class WordComponent(L.LightningWork):
    def __init__(self, word):
        super().__init__(parallel=True, cache_calls=False)  # <-- updated
        self.word = word

    def run(self):
        print(self.word)
```

默认情况下，LightningWork 组件只执行一次，除非其输入参数发生变化。要覆盖这一设置，我们设置 `cache_calls=False`。然而，这样一来，在我们先前定义的 LightningFlow 中，`self.hello.run()` 会一直不停地运行下去，而 `self.world.run()` 得不到运行的机会

```python
class MyRootComponent(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.hello = WordComponent("Hello")
        self.world = WordComponent("World")
        self.counter = 0

    def run(self):
        self.counter += 1
        if self.counter <= 6:
            print("I just go with the Flow!")
        self.hello.run()   # <-- never exits without `parallel=True`
        self.world.run()
```

所以，除了 `cache_calls=False` 之外，我们还在 `WordComponent` 中设置了 `parallel=True`。让我们试试这个更新后的 App，看看会发生什么！

（这个 App 的完整代码可以在[这里](https://github.com/rasbt/srgan-lightning-blog/blob/main/part1-code/minimal-app/app2.py)找到。）

![Lightning app srgan 1 run app2](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/run-app2.gif)

如我们所见，输出现在在 `Hello` 和 `World` 之间交替——这是由 LightningFlow 编排的两个独立进程。

作为附加练习，我鼓励读者尝试全部 4 种组合：

1. `parallel=False, cache_calls=True`（默认设置。也是 `app.py` 中的设置）
2. `parallel=False, cache_calls=False`
3. `parallel=True, cache_calls=True`
4. `parallel=True, cache_calls=False`（`app2.py` 中的设置）

公平地说，我们的 Hello World App 并不是一个非常典型的 App。例如，在真实场景中，你的 `self.hello` 组件可能是一个训练脚本，而 `self.world` 可能包含部署我们模型的指令。这样，部署就不会发生在模型完成训练之前。

虽然上面的代码示例相当枯燥，但我希望它们有助于阐明 Lightning 框架的更宏观概念。我保证下一节会更有意思一点，因为我们将构建一个超分辨率 GAN 研究演示。

---

**Q&A：LightningFlow 与 LightningWork——何时使用哪个？**

LightningFlow 真的只用于编排。任何主要的计算都应该放在 LightningWork 组件中进行。

---

## 开发超分辨率 App

在本节中，我们将构建一个简单的研究演示。为此，我们将使用 PyTorch 实现的超分辨率 GAN。当然，在现实世界中，这可以是您自己的模型。你也可以把模型训练作为 Lightning App 的一部分（就像[PyTorch Lightning App](https://lightning.ai/app/WYU6CrDIAS-PyTorch%20Lightning%20App)中所做的那样。）

### 设置文件结构

为了简单起见，也为了把重点放在理解如何构建一个简单的自定义 Lightning App 上，我们将使用[这个 GitHub 仓库](https://github.com/Lornatang/SRGAN-PyTorch)中的超分辨率 GAN。（为什么选这个仓库？这真的只是一个随意的选择；我只是搜索了"Superresolution GAN"，它就出现了。）

所以，由于我们不训练模型、只是以推理模式运行它，我们只需要这个仓库中的几个文件：图像处理代码、模型本身以及模型权重。

![Lightning app srgan 1 superres filestruct](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/superres-filestruct.webp)

我们将要构建的 App 应当有三个标签页：

1. 演示界面（这里我们使用 Gradio 来实现）；
2. 一个链接到研究论文的标签页；
3. 一个简单的"About"页面。

![Lightning app srgan 1 overview](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/overview.webp)

我们将在下一节中看到如何为这个 App 编写代码。

### 创建 App.py 文件

在本节中，我们将讨论 `app.py` 文件的内容。不过，我们会稍微打乱顺序来讲，所以我建议先在 GitHub 上的[这里](https://github.com/rasbt/srgan-lightning-blog/blob/main/part1-code/superres-local/app.py)查看完整代码。

#### RootFlow

我们先来看看 RootFlow：

```python
class RootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.demo = SRGAN()
        self.about_page = ChildFlow()

    def run(self):
        self.demo.run()

    def configure_layout(self):
        tab_1 = {"name": "SRGAN Demo", "content": self.demo}
        tab_2 = {
            "name": "SRGAN Paper",
            "content": "https://arxiv.org/pdf/1609.04802v5.pdf",
        }
        tab_3 = {"name": "About", "content": self.about_page}
        return tab_1, tab_2, tab_3

app = L.LightningApp(RootFlow())
```

在 `__init__` 构造函数中，我们指定了两个组件：

1. `self.demo = SRGAN()`，这是一个 LightningWork，负责模型加载和预测。
2. `self.about_page = ChildFlow()`，这是一个 LightningFlow，用于渲染 *About* 页面。

在 `configure_layout` 方法中，我们为 App 指定了 3 个标签页：主演示页面、SRGAN 研究论文的链接，以及项目 About 页面。

在 `run` 方法中，我们执行 `SRGAN` work 组件，我们马上就会看到它。

#### SRGAN Work 组件

现在让我们看看用于在上面 RootFlow 中构建演示的 `SRGAN` 类：`self.demo = SRGAN()`。

---

**关于用 TorchHub 简化模型代码的说明**

这段代码可能看起来有点繁琐，但那是因为使用 SRGAN 模型需要几行代码。如果 SRGAN 与 [PyTorchHub](https://pytorch.org/hub/) 兼容，我们本可以省下几行代码，像使用其他新近研究模型那样直接加载它。不过，让模型与 PyTorchHub 兼容是另一个话题了。

```python
model = torch.hub.load('facebookresearch/deit:main', 'deit_base_patch16_224', pretrained=True)
model.predict(...)
```

---

下面的 `SRGAN` 代码子类化自 [`ServeGradio`](https://lightning.ai/lightning-docs/api_reference/generated/lightning_app.components.serve.gradio.ServeGradio.html#servegradio)，它是面向 [Gradio](https://gradio.app) 的一个 LightningWork 组件：

```python
import cv2
import gradio as gr
from lightning.app.components.serve import ServeGradio
import torchvision.transforms as T

# Local files:
import imgproc
from model import Generator

class SRGAN(ServeGradio):

    inputs = gr.inputs.Image(type="pil", label="Select an input image")  # required
    outputs = gr.outputs.Image(type="pil")  # required
    examples = ["./examples/comic_lr.png"]  # required

    def __init__(self):
        super().__init__()
        self.ready = False  # required

    def predict(self, img):

        DEVICE = torch.device("cpu")

        # resize image
        height, width = img.size
        print("Original size:", height, width)
        max_size = max(height, width)
        if max_size > 100:
            ratio = 100 / max_size
            new_size = (round(ratio * height), round(ratio * width))
            img = img.resize(new_size)

        new_height, new_width = img.size
        print("Resized size:", new_height, new_width)

        # convert image to tensor
        opencv_image = np.array(img)
        opencv_image = opencv_image[:, :, ::-1].copy()
        lr_image = opencv_image.astype(np.float32) / 255.0
        lr_image = cv2.cvtColor(lr_image, cv2.COLOR_BGR2RGB)
        lr_tensor = imgproc.image2tensor(lr_image, False, False).unsqueeze_(0)
        lr_tensor = lr_tensor.to(device=DEVICE)

        # get upscaled image
        with torch.no_grad():
            sr_tensor = self.model(lr_tensor)
        transform = T.ToPILImage()

        # Remove batch dimension
        sr_tensor.squeeze_(0)
        return transform(sr_tensor)

    def build_model(self):
        WEIGHTS_PATH = "./weights/SRGAN_x4-ImageNet-c71a4860.pth.tar"
        DEVICE = torch.device("cpu")

        # Initialize the model
        model = Generator()
        model = model.to(memory_format=torch.channels_last, device=DEVICE)
        print("Build SRGAN model successfully.")

        # Load the SRGAN model weights
        checkpoint = torch.load(WEIGHTS_PATH)
        model.load_state_dict(checkpoint["state_dict"])
        print(f"Load SRGAN model weights `{WEIGHTS_PATH}` successfully.")
        model.eval()

        return model
```

（去 Component Gallery 看看已有哪些组件吧。在第 3 部分中，我们将学习如何构建自己的组件。）

`SRGAN` 由两个主要方法组成：`predict` 和 `build_model`。

`build_model` 方法定义了如何从检查点路径加载 SRGAN 模型。请注意，`build_model` 方法中的代码取决于[SRGAN GitHub 仓库](https://github.com/Lornatang/SRGAN-PyTorch)中模型的实现方式。这里是一个 PyTorch 模型，但值得强调的是，它可以是任何东西：scikit-learn 模型、TensorFlow 模型，或者 Jax/Flax 模型。重要的是 `build_model` 返回一个可用于输入数据的模型。

`predict` 方法随后使用加载的模型，以推理模式运行它来放大图像。这里有很多代码，其中大部分基于 SRGAN GitHub 仓库中的代码示例。对于你自己的模型，这可能会简单得多。

注意，出于效率考虑，我添加了一小段调整输入尺寸的代码。这是因为 SRGAN 实现对大尺寸输入图像需要大量 RAM。这段 resize 代码会对输入图像重新缩放，使最长边（高度或宽度）不超过 100 像素。

`SRGAN` 类顶部的几行：

```python
inputs = gr.inputs.Image(type="pil", label="Select an input image")  # required
outputs = gr.outputs.Image(type="pil")  # required
examples = ["./examples/comic_lr.png"]  # required
```

是 [ServeGradio](https://lightning.ai/lightning-docs/api_reference/generated/lightning_app.components.serve.gradio.ServeGradio.html?highlight=servegradio#lightning_app.components.serve.gradio.ServeGradio) 组件特有的。在第 3 部分中，我们将对 ServeGradio 组件做一些自定义，以学习如何采用并开发我们自己的组件。不过，在你走这条路、考虑开发自己的组件之前，我建议先看看 [Component Gallery](https://lightning.ai/components/)：

![Lightning app srgan 1 component gallery](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/component-gallery.webp)

### About 页面前端

在 RootFlow 中，我们把 `about_page` 定义为一个 `ChildFlow()`：

```python
class RootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()

        self.demo = SRGAN()
        self.about_page = ChildFlow()  # <-- here!

    def run(self):
        self.demo.run()

    def configure_layout(self):
        tab_1 = {"name": "SRGAN Demo", "content": self.demo}
        tab_2 = {
            "name": "SRGAN Paper",
            "content": "https://arxiv.org/pdf/1609.04802v5.pdf",
        }
        tab_3 = {"name": "About", "content": self.about_page}  # <--
        return tab_1, tab_2, tab_3
```

在这里，ChildFlow 是一个配置了 [Streamlit](https://streamlit.io) 前端的 LightningFlow。如果你以前用过 Streamlit，你可能会觉得仅仅渲染一个简单的 markdown 页面就动用它是杀鸡用牛刀。不过，我认为在这里用 Streamlit 作为占位符很有意思，万一你想采用它来构建更花哨的东西呢。当然，还有许多其他前端可供选择，从 Jupyter Notebook 到 React.js：

![Lightning app srgan 1 frontends](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/frontends.webp)

Streamlit 前端按如下方式配置，我们在这里配置 RootFlow 中使用的 ChildFlow——这也是一个我们可以拥有多个 LightningFlow 组件的好例子：

```python
def your_streamlit_app(lightning_app_state):
    static_text = """
    # SRGAN Lightning App

    This is a simple [Lightning app](https://lightning.ai) that runs
    SRGAN model based on [this](https://github.com/Lornatang/SRGAN-PyTorch)
    GitHub repository.

    If you want to learn more about Lightning Apps, checkout the official
    [lightning.ai](https://lightning.ai) website.

    If you have any questions or suggestions, you can find
    me [here](https://sebastianraschka.com) and
    [here](http://twitter.com/rasbt).
    """
    st.write(static_text)

class ChildFlow(L.LightningFlow):
    def configure_layout(self):
        return StreamlitFrontend(render_fn=your_streamlit_app)
```

### 运行超分辨率 App

由于这个项目在图像预处理步骤中涉及 PyTorch 和 OpenCV，我们将不得不安装更多依赖。要获得我撰写本文时使用的确切版本号，我建议直接通过 GitHub 仓库中的 [requirement.txt](https://github.com/rasbt/srgan-lightning-blog/blob/main/part1-code/superres-local/requirements.txt) 安装：

```python
conda create -n superres python=3.8
conda activate superres

pip install -r https://raw.githubusercontent.com/rasbt/srgan-lightning-blog/main/part1-code/superres-local/requirements.txt?token=GHSAT0AAAAAABUUA7E3SBDECAJWVHD7AHC2YVKLPJA
```

现在我们应该准备就绪了，让我们运行我们的 App，看看它是否工作：

```python
lightning run app app.py
```

（要在你自己的机器上本地试用这个 App，我建议从 [GitHub 仓库](https://github.com/rasbt/srgan-lightning-blog/tree/main/part1-code/superres-local)获取文件。）

![Lightning app srgan 1 demo](https://sebastianraschka.com/images/blog/2022/lightning-app-srgan-1/demo.gif)

## 下一步：把 App 部署到云端

在本文中，我们探索了 Lightning 框架的核心组件，并构建了我们的第一个 Lightning App。在本地运行 Lightning App 只是乐趣的一半。Lightning 真正大放异彩的地方在于，它让我们能够以超级简单的方式访问云计算资源来分享 App——如果你愿意，甚至可以训练模型。请期待下一篇文章！

PS：如果你不想等，直接运行

```python
lightning run app app.py --cloud
```

然后看魔法发生吧。
