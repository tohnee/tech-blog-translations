---
title: "让 Claude 成为更好的电气工程师"
title_en: "Making Claude a better electrical engineer"
date: 2025-12-12
source: https://claude.com/resources/articles/making-claude-a-better-electrical-engineer
crawled: 2026-11-17
translated: 2026-11-17
---

# 让 Claude 成为更好的电气工程师

> 原文：[Making Claude a better electrical engineer](https://claude.com/resources/articles/making-claude-a-better-electrical-engineer) · Claude 博客

与定制电路板制造商等领域专家合作，如何帮助我们训练 Claude 更高效地处理专业任务。

[Diode Computers](https://www.diode.computer/) 用 AI 设计和制造定制电路板。Diode 的工具链把电路板设计变成一个软件问题；正如软件工程师借助 Claude Code 之类的工具可以大幅提升效率，Diode 也在把同样的方法用到电气工程师身上，帮助他们在数小时内设计出可直接投产的电路板。

Diode 开发并维护 [Zener 语言](https://github.com/diodeinc/pcb/blob/main/docs/pages/spec.mdx)——一种构建在 [Starlark](https://github.com/bazelbuild/starlark) 之上的领域特定语言，用于描述印制电路板（PCB）原理图；以及 [pcb](https://github.com/diodeinc/pcb?tab=readme-ov-file)——它使用 Zener 语言在 KiCad 之上提供各种自动化能力。

对电气工程师来说，一项重要工作是构建参考设计：当设计者想使用某款芯片时，需要依靠数百页的文档来弄清这颗芯片要正常工作需要哪些元件。一颗典型的芯片可能需要多达十几个外围元件——电阻、电容、电感之类——而关于如何把它们连接起来，结构良好的信息往往相当稀少。

电气工程师已经在用 Claude Code，从非结构化文档中自动生成 Zener 格式的参考设计，然后再交由人工审阅。但考虑到这一环境的独特性——它包含领域专用工具，并要求深厚的专业领域知识——Claude 在自动生成参考设计这一任务上的智能体表现，以及它对该具体电气工程任务的整体理解，仍有提升空间。在自动生成参考设计时，常见的失败模式包括：

* 漏掉数据手册中关于电路应如何配置的细节
* 错误解读参考原理图图片
* 误解或误用 Zener

当我们发现 Claude 在需要深厚专业知识的领域任务上存在能力缺口时，可以与该领域的专家合作，教 Claude 改进这些任务的表现。这些知识会被编码进公开发布的 Claude 模型中，让所有使用 Claude 模型的用户都从中受益——无论是在 Claude Code 中、在 [claude.ai](http://claude.ai) 上，还是在他们自己由 Claude 驱动的系统和应用中。

![](https://assets.claude.com/36085fc061541b291ec9e1652f00fe3948518aa7.png)

工程师正在处理一块借助 Claude 设计的印制电路板。图片来源：Diode Computers。

## 界定问题范围

我们与 Diode 启动了一项联合计划，以理解并提升 Claude 自动生成参考设计的能力。在这个智能体任务中，Claude 以某颗芯片的文档为输入，输出一份完整的 Zener 参考设计。要正确完成这一点，Claude 必须通读大量文档，理解密集的技术写作内容和图表，并编写一份完整的、可配置的原理图，完整表达该芯片的所有配置和运行模式。在这一智能体设置中，Claude 可以使用读写文件和执行 bash 命令的工具，并能访问 Zener 编译器、该语言的文档以及少量示例，除此之外没有其他资源。

判断一份参考设计是否正确同样不容易。文档对运行时究竟需要哪些具体元件和参数往往说明不足。为此，每份参考设计都用一个定制的*测试台（testbench）*来评分：它不做关于单个元件是否存在的绝对断言（例如「电源与地之间有一个 20uF 电容」），而是编码更高层级的要求（例如「电源与地之间至少有 22uF 电容」）。这样可以确保模型得到的信号既准确，又不过度受限。

在这个定义清晰、且成功与失败的判定标准也清晰的任务上，我们与 Diode 合作，把相关改进引入 Sonnet 4.5 及后续 Claude 模型的训练中，使其更好地自动生成电路板参考设计。

## 基准测试结果

为了对 Claude 在该任务上的表现做基准测试，我们用一组生成的参考设计，在 Claude Opus 4.1、Claude Sonnet 4 和 Claude Sonnet 4.5 之间做了盲测两两对比。我们发现，Diode 的电气工程师在 10 次中有 8 次更青睐 Claude Sonnet 4.5 生成的参考设计。与其他模型相比，Claude Sonnet 4.5 更善于捕捉文档材料中的细微之处，也更善于遵循其工具链的约定与语义。

![](https://assets.claude.com/8e826d984e89f6e086f159955b564d56617e2539.png)

在盲测两两对比中，Diode 的电气工程师更偏好 Sonnet 4.5 的参考设计，而非 Opus 4（60% 对 40%）和 Sonnet 4（82% 对 18%）的版本。

## 未来方向

与 Diode 的这种合作模式，可以复制到任何领域或行业的任何公司——只要 Claude 以智能体方式部署在成功与失败标准清晰的任务上。Anthropic 一直在持续改进 Claude，让它成为横跨尽可能广泛领域与行业的最佳虚拟协作者。那些需要深厚专业知识、依赖领域特定流程、工具和工作流的任务与工作流，都是与 Anthropic 深入合作的理想候选。

如果你有兴趣与 Anthropic 合作改进未来版本的 Claude，[请填写这份表格](https://docs.google.com/forms/d/e/1FAIpQLScs9kVDB_PRyXPueayJ0c4pKUGwFdDwrKlRPsniVXCqw0utQQ/viewform?usp=dialog)，我们会与你联系。

## 致谢

本文由 Diode Computers 的 Davide Asnaghi、Lenny Khazan 与 Anthropic 的 Connor Jennings、David Hershey、Nicholas Marwell 合作撰写。
