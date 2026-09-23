---
title: "CrypTen：基于 PyTorch 的安全机器学习新研究工具"
title_en: "Crypten: A new research tool for secure machine learning with PyTorch"
date: 2019-10-10
source: http://ai.facebook.com/blog/crypten-a-new-research-tool-for-secure-machine-learning-with-pytorch
crawled: 2026-09-22
translated: 2026-09-22
---

# CrypTen：基于 PyTorch 的安全机器学习新研究工具

> 原文：[Crypten: A new research tool for secure machine learning with PyTorch](http://ai.facebook.com/blog/crypten-a-new-research-tool-for-secure-machine-learning-with-pytorch) · Meta AI（Wayback 存档）

2019 年 10 月 10 日

尽管 AI 社区近来在推进机器学习应用方面取得了巨大进展，但目前可用于构建能处理加密数据的 ML 系统的工具仍非常有限。这制约了 ML 在出于安全原因必须加密的领域中的应用，例如涉及敏感医疗信息的工作，或者人们仅仅为了额外隐私而希望加密的数据。如今构建满足这些用例的安全 ML 系统非常困难，甚至不可能，因为强大且易用的框架无法有效处理加密数据。

为满足这一需求并加速该领域进展，Facebook AI（FAIR，Meta 基础人工智能研究院）的研究者构建并正在开源 CrypTen——一个新的、易用的软件框架，基于 PyTorch 构建，旨在促进安全与隐私保护机器学习的研究。CrypTen 让通常并非密码学专家的 ML 研究者，能够轻松地使用安全计算技术试验 ML 模型。通过利用 PyTorch 并与之集成，CrypTen 降低了已熟悉其 API 的 ML 研究者和开发者的门槛。AI 研究者可以用 CrypTen 在加密数据上训练 ResNet 之类的 PyTorch 模型，同时保持 Torch 张量熟悉的观感。例如：

```python
x = torch.tensor([1, 2, 3]
y = torch.tensor([4, 5, 6])
z = x + y
```

可以按如下方式改写：

```python
x_enc = crypten.cryptensor([1, 2, 3])
y_enc = crypten.cryptensor([4, 5, 6])
z_enc = x_enc + y_enc
```

CrypTen 在数千名 ML 研究者已熟悉的 PyTorch 平台，与长期以来关于能有效处理加密数据的算法和系统的学术研究之间架起了一座桥梁。对于探索这一领域的 AI 研究社区而言，前路仍然漫长，因为安全计算技术存在各种权衡，例如更高的计算和通信开销，或受限的函数空间。但我们相信 CrypTen 将帮助学术界和产业界的研究者迈向这样一个未来：安全计算技术成为 ML 框架本身的组成部分，研究者和工程师在需要时可以无缝切换到隐私保护 ML。

我们随 PyTorch 开发者大会上展示的其他新研发工具一起发布 CrypTen。CrypTen 已在此提供，更多技术细节见 CrypTen 网站。

## CrypTen 的基本组件

CrypTen 目前实现了一种名为安全多方计算（MPC）的密码学方法，我们预计在后续版本中增加对同态加密和安全飞地（secure enclave）的支持。MPC 与如今广泛使用的 RSA、AES 等密码学协议的不同之处在于，它允许在保护隐私的同时对加密数据进行计算。我们在密码学研究中常用的「诚实但好奇」（假设不存在恶意与对抗性参与者）模型下实现 MPC，但在 CrypTen 可以用于生产环境之前，还必须添加额外的防护措施。

（原文此处附图：CrypTen 的高层概览，其中数据和模型都使用 MPC 加密。）

与以往的安全计算协议实现相比，CrypTen 为 ML 研究者提供三大益处：

- **它以机器学习为先。**框架通过 CrypTensor 对象呈现这些协议，其观感与 PyTorch 张量完全一致。这使用户能够使用与 PyTorch 类似的自动微分和神经网络模块。这有助于让任何用过 PyTorch 的人都能使用安全协议。
- **CrypTen 是基于库的。**与该领域的其他软件不同，我们没有实现编译器，而是像 PyTorch 那样实现了一个张量库。这使人们更容易调试、试验和探索 ML 模型。
- **该框架以真实世界挑战为出发点构建。**CrypTen 没有缩减或过度简化安全协议的实现。各方在相互通信的独立进程中运行，也可以在不同的机器上运行。虽然 CrypTen 目前尚未达到生产可用状态，但它可以就使用安全协议做机器学习所需的计算与通信开销提供贴近现实的洞察，从而促进高质量研究。

以下代码片段展示了用加密模型对加密数据进行推理的示例。

PyTorch 主片段：

```python
data = torch.load(DATA_PATH)
model = torch.load(MODEL_PATH)
model.eval()
output = model(data)
```

CrypTen 主片段：

```python
data_enc = crypten.load(DATA_PATH, src=1)
model = crypten.load(PATH, dummy_model=ModelClass(), src=0)
dummy_input = torch.empty(data_enc.size())
private_model = crypten.nn.from_pytorch(model, dummy_input).encrypt(src=0)
private_model.eval()
output_enc = private_model(data_enc)
```

发布之初，CrypTen 覆盖从简单线性模型到 ResNet 的模型，我们正朝着与 PyTorch 全部模型对齐的方向努力。

（原文此处附图：该示例展示 MPC 如何通过在多个参与方之间拆分数据来加密信息，每一方都可以对自己的份额（分别为 5 和 7）执行计算，但无法读取原始数据（12）。随后每一方执行计算（「乘以 3」）。当输出被合并时，结果（36）与直接对数据执行计算的结果完全一致。由于参与方 A 和参与方 B 都不知道最终结果（36），它们无法推断出原始数据点（12）。）

（原文此处嵌入视频/图示：该图展示如何使用 MPC 调整照片，而任何一方都无法访问图像内容。）

## 机器学习需要安全计算工具

如今的机器学习系统通常可以在设备上安全运行——例如将语音转录为文本或将一种语言翻译成另一种语言。但在这些模型部署之前，它们通常在公开可用的数据（如维基百科条目）或已获授权使用的数据集（如 ImageNet）上训练。然而在许多情况下，训练所需的数据要么过于敏感而无法共享，要么存在安全、隐私、政策或法律上的障碍。例如，医学研究者在基因数据上进行人群研究时常面临严峻挑战，因为这类数据非常敏感，难以在研究机构之间共享。类似地，由于共享薪资数据的隐私顾虑，研究公司间的性别薪酬差距也很困难。

MPC 等安全计算技术为这些问题提供了可能的解决方案，允许各方以安全的方式加密自己的数据，同时仍允许对加密数据进行聚合的 ML 计算。尽管 MPC 使这类用例成为可能，但由于缺乏能够抽象掉技术复杂性的熟悉 ML 框架，用 MPC 做 ML 研究一直颇具挑战。CrypTen 通过向 ML 研究者提供一个熟悉的抽象来满足这一需求。

## 示例用途与应用

CrypTen 可以加载预训练的 PyTorch 模型，让用户灵活地加载现有模型用加密数据做推理。用户还可以用熟悉的 PyTorch API 训练加密模型。该框架支持快速增加的 PyTorch 张量算子子集，用户可以用它们构建 ResNet 之类的模型。

（原文此处嵌入视频/图示：该图展示 CrypTen 如何通过用加密张量替换标准 PyTorch 张量，让研究者轻松使用 PyTorch 模型。虚线表示我们预计将来添加到 CrypTen 的潜在扩展。）

CrypTen 可以与任意数量的参与方执行 MPC，还可以在算术分享与二进制（XOR）分享之间转换，从而无需任何近似即可实现 ReLU 等常见非线性。这也使 max 等操作成为可能，而后者是上下文老虎机（contextual bandit）模型所必需的。

安全计算技术因计算和通信量的增加而带来性能下降的挑战。CrypTen 通过在必要时将功能下沉到 PyTorch 核心来应对，例如在 PyTorch 本身中增加对 int64 等数据类型的支持。深度学习系统必须能够在规模上高效运行，因此我们将在后续版本中持续改进性能。

这些能力使 Facebook 研究者得以用 CrypTen 构建隐私保护的上下文老虎机模型。上下文老虎机模型用于许多推荐系统中：参与方根据关于环境的特定上下文选择一个臂（arm），然后因其动作获得奖励。参与方将奖励作为学习信号，目标是最大化总奖励，从而解决推荐或排序问题。在这一场景的隐私保护变体中，每一方都有不愿与其他方共享的上下文。CrypTen 使我们能够在尊重这一要求的前提下训练模型。每一方加密自己的上下文，并使用加密模型选择一个臂。被选中的臂只对拉臂的那一方公开。随后另一方获得奖励，该奖励信号被加密并用于学习加密模型，从而闭合学习回路。

上下文老虎机模型具有若干对许多基于 MPC 的系统而言颇具挑战的特性。参与方数量可以是任意的，而许多 MPC 协议是专为恰好两方设计的。这些模型涉及对 MPC 有挑战的计算，例如除法、指数运算和求最大值。CrypTen 与多方可用的能力、算子的高效实现、在加法分享与 XOR 分享之间来回切换（使 max 等算子成为可能）的能力，以及熟悉的 PyTorch API，使我们得以快速训练此类模型。

## 加速 ML 安全计算框架的研究

机器学习在过去十年取得了巨大进展，部分归功于数据和算力的可得性，以及易用框架的发展。我们希望通过开发 CrypTen 这样的工具并降低其他研究者的进入门槛，帮助培育和加速面向机器学习的新安全计算技术研究。

**作者**

- David Gunning，技术项目经理
- Awni Hannun，研究科学家
- Brian Knott，研究工程师
- Laurens van der Maaten，研究科学家
- Vinicius Reis，研究工程师
- Shubho Sengupta，软件工程师
- Shobha Venkataraman，软件工程师
- Xing Zhou，AI 研究工程
