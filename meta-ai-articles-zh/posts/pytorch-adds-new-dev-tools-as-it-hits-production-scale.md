---
title: "PyTorch 达到生产规模，新增开发工具"
title_en: "PyTorch adds new dev tools as it hits production scale"
date: 2019-05-01
source: https://ai.facebook.com/blog/pytorch-adds-new-dev-tools-as-it-hits-production-scale
crawled: 2026-09-22
translated: 2026-09-22
---

# PyTorch 达到生产规模，新增开发工具

> 原文：[PyTorch adds new dev tools as it hits production-scale](https://ai.facebook.com/blog/pytorch-adds-new-dev-tools-as-it-hits-production-scale) · Meta AI（Wayback 存档）

自几个月前发布以来，PyTorch 1.0 作为强大、灵活的深度学习平台被快速采用，帮助工程师和研究人员从研究快速走向生产。作为今年 Facebook F8 大会的一部分，我们重点介绍 AI 工程和研究社区使用 PyTorch 1.0 的一些方式，分享最新版本 PyTorch 1.1 的新细节，并展示社区创建的一些新开发工具。

在 2017 年初次发布的基础上，Facebook 与 AI 社区合作于去年 12 月交付了 PyTorch 1.0 稳定版。除了增强的生产导向能力和与领先云平台的深度集成，PyTorch 1.0 还扩展了这个开源库的核心特性，加入了 PyTorch JIT（即时编译），可在即时模式与图模式之间无缝切换，兼顾灵活性与速度。各行业的领先企业开始使用 PyTorch 促进研究，并在翻译、计算机视觉、对话界面、制药研究、工厂优化和自动驾驶研究等应用上大规模部署。社区对 PyTorch 的采用也在持续扩大：斯坦福、UC 伯克利、加州理工等大学把 PyTorch 用作机器学习（ML）课程的基础工具；支持 PyTorch 开发的新生态项目相继启动；主要云平台扩展了与 PyTorch 的集成。

## 跨行业使用 PyTorch

Facebook 目前在用 PyTorch 1.0 的端到端工作流大规模构建和部署翻译与自然语言处理（NLP）服务。这些系统每天为 Messenger 实时翻译等应用提供近 60 亿次翻译，并作为 PyText 的基础，驱动依赖多任务学习的复杂 NLP 模型。

PyTorch 的统一框架让我们能更快地迭代 ML 系统。我们利用即时前端 API（define-by-run）构建神经机器翻译（NMT）模型，充分灵活地探索设计空间、在分布式系统上训练并迭代，最后生成带各种优化（如算子融合等）的图用于生产推理。这一整体工作流展示了 PyTorch 1.0 在大规模生产中的全部威力。

迁移到 PyTorch 还带来了其他好处：研究和生产共用单一代码库，降低了复杂度。这帮助我们的研究人员和产品团队走得更近，总体上让 Facebook 的团队显著加速了从研究到生产的周期，为产品用户带来更好的体验。Facebook 各团队正在为多种领域积极开发端到端 PyTorch 方案，我们在计算机视觉、语音识别和语音合成方面的 PyTorch 项目也在快速推进。

在 Facebook 之外，许多领先企业正在转向 PyTorch 1.0，以加速新 AI 系统的开发和部署。以下是一些例子：

- **Airbnb** 利用 PyTorch 丰富的对话式 AI 库和 API，部署了智能回复（Smart Reply），帮助公司客服更有效地回应客户。
- **ATOM** 正在构建一个平台，以远快于常规流程的速度、更高的成功率生成和优化新药候选。借助 PyTorch 等机器学习框架，ATOM 设计了一个变分自编码器来表示多样的化学结构并设计新药候选。
- **Genentech** 利用 PyTorch 灵活的控制结构和动态图训练深度学习模型，助力个体化癌症疗法的开发。
- **Microsoft** 在整个组织内使用 PyTorch 大规模开发 ML 模型，并通过 ONNX Runtime 部署。Microsoft Cognition 用 PyTorch 构建了可扩展到数十亿词的分布式语言模型，现已用于认知服务等产品中。
- **丰田研究院（TRI）** 正在通过 Toyota Guardian 和 Toyota Chauffeur 技术双管齐下推进自动驾驶。TRI 的机器学习团队正在创建新的深度学习算法，以利用丰田每年 1,000 万辆销售的数据优势。PyTorch 的灵活性极大加速了他们的探索步伐，其新的生产特性将支持更快地向安全关键应用部署。

在 2018 年 12 月发布 PyTorch 1.0 之后，我们现在宣布 v1.1 可用。它改进了性能，添加了新的模型理解与可视化工具以提升易用性，并提供新的 API。PyTorch v1.1 的关键特性包括：

- **TensorBoard**：一等且原生的 TensorBoard 可视化与模型调试支持——TensorBoard 是一个用于检查和理解训练运行与图的 Web 应用套件。PyTorch 现在只需一条简单的「from torch.utils.tensorboard import SummaryWriter」命令即可原生支持 TensorBoard。
- **JIT 编译器**：即时（JIT）编译的改进，包括若干缺陷修复以及 TorchScript 能力的扩展，如对字典、用户类和属性的支持。
- **新 API**：支持布尔张量，并更好地支持自定义循环神经网络。
- **分布式训练**：改进了 CNN 等常见模型的性能；新增对多设备模块的支持，包括把模型切分到多块 GPU 上同时仍使用分布式数据并行（DDP）；并支持并非每次迭代都用到的参数的模块（如控制流、自适应 softmax 等）。请参阅最新教程。

我们还继续与社区合作，培育旨在支持 ML 工程师的项目和工具，覆盖从改进模型理解到用 AutoML 方法自动调优等各种需求。AutoML 方法对 Facebook 的计算机视觉和个性化等应用很有价值。随着 Ax 和 BoTorch 的发布（见下文），我们将分享部分核心算法，包括基于历史任务高效优化超参数的元学习。我们很高兴看到这项工作开源供社区构建。

这一项目与工具的生态既包括 Facebook 已在生产规模部署的开源资源，也包括我们与 Google 等行业领袖合作提供的产品与服务——他们与我们共享开放协作的 AI 社区愿景。以下是一些最新的工具：

- **BoTorch**：BoTorch 是构建在 PyTorch 之上的研究框架，提供贝叶斯优化——一种对评估成本高昂的黑盒函数进行序贯优化的样本高效技术。
- **Ax**：Ax 是一个管理自适应实验的 ML 平台。它让研究人员和工程师能够系统性地探索大型配置空间，以优化机器学习模型、基础设施和产品。
- **PyTorch-BigGraph**：PBG 是一个分布式系统，为拥有数十亿实体和数万亿条边的超大规模图创建嵌入。它支持分片和负采样，并提供基于 Wikidata 嵌入的示例用例。
- **Google AI Platform Notebooks**：AI Platform Notebooks 是 Google Cloud Platform 新推出的托管 JupyterLab 服务。数据科学家可以快速创建预装最新版 PyTorch 的 JupyterLab 虚拟机。它与 BigQuery、Cloud Dataproc、Cloud Dataflow 和 AI Factory 等 GCP 服务紧密集成，让人无需离开 JupyterLab 即可执行完整的 ML 周期。

我们也高兴地看到更广泛的 PyTorch 社区涌现出许多有趣的新项目，亮点包括：

- **BigGAN-PyTorch**：这是一个完整的 PyTorch 重实现，利用梯度累积在少至四块 GPU 上获得大批量的好处。
- **GeomLoss**：一个定义 PyTorch 层的 Python API，用于采样测度、图像和体积之间的几何损失函数，包括 MMD、Wasserstein、Sinkhorn 等。下图展示了用 GeomLoss 生成的 2D 梯度流，适用于处理（任意维度的）点云、密度图和体积分割掩码。
- **PyTorch Geometric**：一个面向 PyTorch 的深度学习扩展库，提供多篇已发表论文中的图及其他不规则结构深度学习（也称几何深度学习）方法。
- **Curve-GCN**：一种实时交互式图像标注方法，使用端到端训练的图卷积网络（GCN）。它支持多边形或样条两种物体标注方式，提升直线型和弯曲物体的标注效率。Curve-GCN 的运行速度比 Polygon-RNN++ 等传统方法快 10 倍。

## Udacity、fast.ai 等开发新的 PyTorch 资源

PyTorch 非常适合教学 ML 开发：它凭借灵活的动态编程环境和友好的 Pythonic 接口支持快速实验。此外，Google Colab 现在提供原生支持 PyTorch 的交互式 Jupyter Notebook 环境，开发者可以用免费的 CPU 和 GPU 资源立即运行任何 PyTorch 教程。

大学课程——包括斯坦福 NLP、UC 伯克利计算机视觉和加州理工机器人课程——现在都在用 PyTorch 授课。此外，大规模开放在线课程（MOOC）正在培养数千名新的 PyTorch 开发者。今天，我们宣布赞助一门新的 Udacity 课程，它建立在去年发布的深度学习导论课程之上。这门新课程由牛津大学和 OpenMined 的 Andrew Trask 主讲，涵盖 AI 隐私方面的重要概念，包括差分隐私和联邦学习等方法。Facebook 还将提供奖学金，支持学生在 Udacity 完整的 Nanodegree 项目中继续 ML 学习。

fast.ai 社区也在持续为 PyTorch 投入精力和资源。6 月，fast.ai 将推出名为「Deep Learning from the Foundations」的新课程，向开发者展示如何从零开始编写矩阵乘法，一路到训练和实现最先进的 ImageNet 模型。课程将深入剖析 PyTorch 和 fast.ai 库中方法的底层实现，并用代码讲解和阐释这些方法背后的学术论文。作为课程的一部分，fast.ai 还将发布新的软件模块，包括 fastai.audio——把 fast.ai 的深度抽象和精选算法带到新的 PyTorch.audio 模块——并展示如何用 fastai.vision 从老电影等素材以及（通过与索尔克研究所合作）前沿显微镜序列创建惊艳的高分辨率视频。此外，fast.ai 还在贡献其新的 X-ResNet 模块，包括一套在 ImageNet 上预训练的模型。

## 开始使用 PyTorch

AI 社区中的每个人——无论是 ML 开发新手，还是寻求加速端到端工作流的研究人员和工程师——都可以访问 pytorch.org、在 Colab 中启动教程，即刻体验 PyTorch。在本地和流行云平台上也有许多轻松上手的方式。随着 Facebook 和 AI 社区中的其他人持续扩展这些资源，PyTorch 将变得更强大、更通用，也更易获取。凭借支持从即时模式追踪和脚本化模型到图模式的混合前端，加上 PyTorch-BigGraph、BoTorch 和 Ax 以及 TensorBoard 支持等不断增长的工具与资源，PyTorch 是把人工智能突破性研究带向生产部署的强大框架。PyTorch 的持续演进是 AI 领域开放、社区主导开发之力量的例证，我们期待未来更多新的协作。

**作者**

- Joe Spisak，Facebook 产品经理
- Jeff Smith，Facebook 工程经理
- Dmytro Dzhulgakov，Facebook 软件工程经理
- Lin Qiao，Facebook 软件工程经理
- Greg Chanan，Facebook 软件工程经理
