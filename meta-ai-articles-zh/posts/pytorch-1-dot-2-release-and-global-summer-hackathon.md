---
title: "PyTorch 1.2 发布，全球夏季黑客马拉松同步开启"
title_en: "PyTorch 1.2 released as Global Summer Hackathon kicks off"
date: 2019-10-10
source: https://ai.facebook.com/blog/pytorch-1-dot-2-release-and-global-summer-hackathon
crawled: 2026-09-22
translated: 2026-09-22
---

# PyTorch 1.2 发布，全球夏季黑客马拉松同步开启

> 原文：[PyTorch 1.2 released as Global Summer Hackathon kicks off](https://ai.facebook.com/blog/pytorch-1-dot-2-release-and-global-summer-hackathon) · Meta AI（Wayback 存档）

上周，研究人员、开发者和工程师齐聚 Facebook 门洛帕克园区，参加两场 PyTorch 夏季黑客马拉松中的第一场。随着 PyTorch 1.2 的发布，参赛者组成团队，用这个开源机器学习（ML）框架的部分最新特性花两天时间构建机器学习项目——包括翻新的领域库和更易上线的生产模型。在这篇文章中，我们重点介绍门洛帕克夏季黑客马拉松的部分获奖项目，并分享如何参加现已开放提交的线上全球夏季黑客马拉松。

## PyTorch 1.2 发布

在 PyTorch 1.0 中，我们引入了 TorchScript，为从即时执行模式的研究原型到图模式的生产部署提供无缝路径。TorchScript 通过把 Python 代码编译或追踪为不依赖 Python 的静态类型图表示来工作，这种表示可以在生产环境中被优化和执行。PyTorch 1.2 带来了更完善的 TorchScript 环境，简化了包含控制流的模型导出，让代码向生产部署的过渡更容易。下面是新的 torch.jit.script() 函数/装饰器的示例：

```python
import torch

class MyModule(torch.nn.Module):
    def __init__(self, N, M):
        super(MyModule, self).__init__()
        self.weight = torch.nn.Parameter(torch.rand(N, M))

    def forward(self, input):
        if input.sum() > 0:
            output = self.weight.mv(input)
        else:
            output = self.weight + input
        return output

# Compile the model code to a static representation
my_script_module = torch.jit.script(MyModule(3, 4))
# Save the compiled code and model data so it can be loaded in C++
my_script_module.save("my_script_module.pt")
```

除这些改进之外，我们还发布了计算机视觉、自然语言处理和语音/音频领域库的新版本。torchvision、torchtext 和 torchaudio 库提供了对常用数据集、变换和最先进模型的便捷访问，帮助研究人员和工程师在这些领域加速开发。访问 PyTorch 博客了解更多关于 PyTorch 1.2 的信息。

## PyTorch 夏季黑客马拉松获胜者

PyTorch 社区的研究人员和开发者参加了在门洛帕克举行的为期两天的 PyTorch 夏季黑客马拉松，构建旨在对人们和企业产生积极影响的应用和模型。我们要感谢所有在本地和世界各地参加黑客马拉松的参与者，他们围绕从天体物理到教育等领域攻坚各种想法。看到如此多样的创新想法和开发速度，实在令人兴奋。以下是部分获奖项目：

- **learn2learn**：learn2learn 是一个 PyTorch 库，旨在让元学习对 ML 开发者更易上手。它包含 MAML 和 Meta-SGD 的实现，以及一个便于创建学习用分布的任务生成器（Task Generator）。
- **HelloWorldNet**：HelloWorldNet 应用 PyTorch 提升系外行星检测的速度和可靠性。它扩展了 Exonet 和 Astronet，并为 Kepler、TESS 和 K2 等数据源提供数据加载器。
- **MineTorch**：MineTorch 是一个供儿童学习并将深度学习模型集成到自己项目中的编程平台。它提供可生成 Python 代码的拖放式用户界面。

## 参加全球夏季黑客马拉松

在门洛帕克两天的黑客马拉松之后，我们宣布举办全球夏季黑客马拉松——一场让世界各地开发者都能轻松参与的线上黑客马拉松。本次黑客马拉松的重点是使用 PyTorch 构建有创意、实现精良、能为企业和人们带来积极影响的解决方案。解决方案可以是 ML 模型、应用或创意项目（如艺术或音乐）。参赛者可从现在到 9 月 16 日提交项目，角逐超过 60,000 美元的现金奖励，并有机会在 2019 年 10 月 10 日的 PyTorch 开发者大会上展示自己的项目。加入线上全球夏季黑客马拉松，从这里开始。

**作者**

- Joe Spisak，Facebook AI 产品经理
- Soumith Chintala，Facebook AI Research 软件工程师
