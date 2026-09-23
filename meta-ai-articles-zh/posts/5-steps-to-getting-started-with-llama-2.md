---
title: "Llama 2 入门五步走"
title_en: "5 Steps to Getting Started with Llama 2"
date: 2023-11-15
source: https://ai.meta.com/blog/5-steps-to-getting-started-with-llama-2
crawled: 2026-09-22
translated: 2026-09-22
---

# Llama 2 入门五步走

> 原文：[5 Steps to Getting Started with Llama 2](https://ai.meta.com/blog/5-steps-to-getting-started-with-llama-2) · Meta AI（Wayback 存档）

人工智能（AI）近来的突飞猛进不仅激发了公众的好奇心，也印证了这一领域的先驱们一直以来的认识：这些技术蕴含着助力我们成就非凡事业的巨大潜力。这种潜力远不止于算法本身；它有望开启经济增长、社会进步以及表达与连接的新模式的新时代。在 Meta，我们坚信开放的 AI 开发方式，尤其是在生成式 AI 这一充满活力的格局中。通过开放共享 AI 模型，我们把它们的益处延伸到社会的每个角落。我们最近开源了 Llama 2，释放了这些大语言模型的力量，让企业、初创公司、有抱负的创业者和研究者都能用上这些工具，从而负责任地实验、创新并规模化你的想法。在这篇博客中，我们将带你探索上手 Llama 2 的五个步骤，让你在自己的项目中利用 Llama 2 的种种好处。我们会讲解关键概念、如何安装设置、可用资源，并提供一个循序渐进的过程来配置和运行 Llama 2。

## 简介

Llama 2 包含预训练和微调大语言模型的模型权重与起始代码，参数规模从 7B 到 70B。Llama 2 的训练数据比 Llama 1 多 40%，上下文长度翻倍。Llama 2 在公开可用的在线数据源上完成预训练。

（图片来自 Llama 2 - Meta AI）

微调模型 Llama-2-chat 利用公开可用的指令数据集和超过 100 万条人工标注，并通过人类反馈强化学习（RLHF）确保安全性与有用性。

（图片来自 Llama 2 - Resource Overview - Meta AI）

Llama 2 在许多外部基准上优于其他开放语言模型，包括推理、编码、熟练度和知识测试。想了解更多关于这些基准及其对比情况，请访问我们的网站，那里有更详细的介绍。Llama 2 可免费用于研究和商业用途。下一节，我们将介绍上手 Llama 2 可以采取的 5 个步骤。本地安装 Llama 2 的方法有很多，我们将介绍其中一种能让你轻松配置并快速开始使用 Llama 的方式。让我们开始吧！

## Llama 2 入门

### 步骤 1：先决条件与依赖

我们将使用 Python 编写脚本来搭建并运行流水线。安装 Python 请访问 Python 官网，在那里你可以选择自己的操作系统并下载喜欢的 Python 版本。运行本示例时，我们将使用 Hugging Face 的 transformers 和 accelerate 库。

```
pip install transformers
pip install accelerate
```

### 步骤 2：下载模型权重

我们的模型可在 Llama 2 Github 仓库获取。通过我们的 Github 仓库下载模型：

1. 访问 Meta AI 官网，接受我们的许可协议并提交表单。请求获批后，你会在电子邮件中收到一个预签名 URL。
2. 克隆 Llama 2 仓库

```
git clone https://github.com/facebookresearch/llama
```

3. 运行 download.sh 脚本（`sh download.sh`）。出现提示时，输入你在电子邮件中收到的预签名 URL。
4. 选择你要下载的模型变体，例如：7b-chat。这会下载 tokenizer.model，以及一个包含权重的 llama-2-7b-chat 目录。
5. 运行 `ln -h ./tokenizer.model ./llama-2-7b-chat/tokenizer.model` 创建指向分词器的链接。这是下一步转换所必需的。
6. 将模型权重转换为可在 Hugging Face 上运行的格式：

```
TRANSFORM=`python -c "import transformers;print('/'.join(transformers.__file__.split('/')[:-1])+'/models/llama/convert_llama_weights_to_hf.py')"`
pip install protobuf && python $TRANSFORM --input_dir ./llama-2-7b-chat --model_size 7B --output_dir ./llama-2-7b-chat-hf
```

我们也在 Hugging Face 上提供了已转换好的 Llama 2 权重。要使用 Hugging Face 上的下载内容，你必须先按上述步骤请求下载权限，并确保使用与你的 Hugging Face 账号相同的电子邮箱。

### 步骤 3：编写 Python 脚本

现在，我们将创建一个新的 Python 脚本来运行示例。该脚本包含加载模型以及用 transformers 运行推理所需的全部代码。

**导入所需模块**

首先，我们需要在脚本中导入以下必需模块：LlamaForCausalLM 是 Llama 2 的模型类，LlamaTokenizer 为模型准备待处理的提示词，pipeline 是一个用于生成模型输出的抽象，torch 则让我们能够使用 PyTorch 并指定想要使用的数据类型。

```
import torch
import transformers
from transformers import LlamaForCausalLM, LlamaTokenizer
```

**加载模型**

接下来，我们用下载并转换好的权重（本示例中存放在 ./llama-2-7b-chat-hf）加载 Llama 模型。

```
model_dir = "./llama-2-7b-chat-hf"
model = LlamaForCausalLM.from_pretrained(model_dir)
```

**定义并实例化分词器和流水线**

我们需要确保模型的输入已准备就绪，这通过加载与模型配套的分词器来完成。在脚本中添加以下代码，从相同的模型目录初始化分词器：

```
tokenizer = LlamaTokenizer.from_pretrained(model_dir)
```

接下来，我们需要一种用模型做推理的方式。pipeline 允许我们指定流水线要运行的任务类型（"text-generation"）、指定流水线做预测所用的模型（model）、定义使用该模型的精度（torch.float16）、以及流水线运行的设备（device_map）等多种选项。在脚本中添加以下代码，实例化我们将用于运行示例的流水线：

```
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    device_map="auto",
)
```

**运行流水线**

现在流水线已定义好，我们需要提供一些文本提示作为流水线的输入，供其运行时生成回复（sequences）。下面示例中的流水线将 do_sample 设为 True，这允许我们指定想用的解码策略，以便在整个词表的概率分布中选择下一个词元。在我们的示例中使用的是 top_k 采样。通过修改 max_length，你可以指定希望生成的回复有多长。把 num_return_sequences 参数设为大于 1，可以生成多个输出。在脚本中添加以下代码，提供输入以及运行流水线的相关信息：

```
sequences = pipeline(
    'I have tomatoes, basil and cheese at home. What can I cook for dinner?\n',
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=400,
)
for seq in sequences:
    print(f"{seq['generated_text']}")
```

### 步骤 4：运行模型

现在脚本已经可以运行了。保存脚本，回到你的 Conda 环境。运行脚本时，输入 `python <脚本名>.py` 并按回车。如下所示，这将下载模型、展示流水线的分步进度，以及运行脚本后我们的提问和生成的回答：

（在本地运行 Llama 2-7B-chat-hf）

你现在可以在本地配置并运行 Llama 2 了。可以在字符串参数中提供不同的提示词来尝试。你也可以在加载模型时通过指定模型名称来加载其他 Llama 2 模型。查看下一节提到的其他资源，进一步了解 Llama 2 的工作原理，以及帮助你上手的各种资源。

### 步骤 5：进一步探索——资源与延伸阅读

- 想进一步了解 Llama 2 的工作原理、训练方式和所用硬件，请阅读我们的论文《Llama 2: Open Foundation and Fine-Tuned Chat Models》，其中更详细地介绍了这些方面。
- 从我们的 Llama 2 Github 仓库获取模型源码，其中展示了模型的工作方式，以及加载 Llama 2 模型和运行推理的最小示例。在那里你会找到下载、设置模型的步骤以及运行文本补全和聊天模型的示例。
- 在模型卡中进一步了解该模型，其中介绍了模型架构、预期用途、硬件与软件要求、训练数据、结果和许可证。
- 查看我们的 llama-recipes Github 仓库，它提供了如何快速上手微调以及如何对微调后模型运行推理的示例。
- 看看 Code Llama——我们最近发布的 AI 编程工具。它是基于 Llama 2 构建并针对代码生成与讨论微调的 AI 模型。访问我们的网站，进一步了解该模型的工作原理、基准测试、技术规格和常见问题。
- 阅读我们的《负责任使用指南》（Responsible Use Guide），它以负责任的方式构建由大语言模型（LLM）驱动的产品提供了最佳实践和注意事项，覆盖从立项到部署的各个开发阶段。

我们希望这篇文章能帮助你掌握上手 Llama 2 所需的步骤。敬请期待我们后续的博客文章，我们将探索其他开源项目以及如何将它们融入你自己的项目。

## 关于本系列

本博客是我们的「入门五步走」系列的一部分，在这一系列中，我们会介绍使用 Meta 的某个开源项目需要采取的 5 个步骤。请留意更多入门博客，我们会讨论更多项目以及如何在你的项目中开始使用它们。想进一步了解 Meta 的 AI，请访问我们的网站、订阅 Meta AI YouTube 频道，或在 X 和 Facebook 上关注我们。想进一步了解 Meta 开源，请访问我们的网站、订阅 Meta 开源 YouTube 频道，或在 X 和 Facebook 上关注我们。

**作者：**Navyata Bawa，开发者布道师

**贡献者：**Suraj Subramanian
