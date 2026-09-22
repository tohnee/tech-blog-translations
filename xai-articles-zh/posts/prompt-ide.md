---
title: "宣布 PromptIDE"
title_en: "Announcing PromptIDE"
date: 2025-03-19
source: https://x.ai/news/prompt-ide
crawled: 2026-09-22
translated: 2026-09-22
---

# 宣布 PromptIDE

> 原文：[Announcing PromptIDE](https://x.ai/news/prompt-ide) · xAI

2023 年 11 月 6 日

面向提示词工程与可解释性研究的集成开发环境。

---

**xAI PromptIDE 是一个面向提示词工程与可解释性研究的集成开发环境。
它通过一个 SDK 加速提示词工程——该 SDK 允许实现复杂的提示词技术，并提供将网络输出可视化的丰富分析工具。
在我们对 [Grok™](/blog/grok) 的持续开发中，我们大量使用它。**

我们开发 PromptIDE 的目的，是向社区中的工程师和研究者透明地开放 Grok-1——驱动 [Grok™](/blog/grok) 的模型。这个 IDE 旨在赋能用户，帮助他们快速探索我们大语言模型（LLM）的能力。IDE 的核心是一个 Python 代码编辑器，它与全新的 [SDK](https://developers.x.ai/python-sdk/) 相结合，可以实现复杂的提示词技术。在 IDE 中执行提示词时，用户可以看到有用的分析信息，例如精确的分词（tokenization）、采样概率、候选 token 以及聚合的注意力掩码。

该 IDE 还提供一系列提升体验的功能。它会自动保存所有提示词，并内置版本管理。运行提示词生成的分析结果可以永久保存，让用户能够比较不同提示词技术的输出。此外，用户可以上传小文件（如 CSV 文件），并用 SDK 中的一个 Python 函数读取它们。结合 SDK 的并发特性，即使是稍大的文件也能快速处理。

我们也希望围绕 PromptIDE 建立一个社区。任何提示词都可以一键公开分享。用户可以自行决定是只分享提示词的某个版本，还是分享整棵版本树。分享提示词时还可以附带任何已保存的分析结果。

PromptIDE 面向我们早期访问计划的成员开放。下面是这个 IDE 主要功能的走读。

谢谢你们，  
xAI 团队

# 代码编辑器与 SDK

![PromptIDE 中的采样概率](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreenshot_42.44d24fa3.webp&w=3840&q=75)

PromptIDE 的核心是一个代码编辑器和一套 [Python SDK](https://developers.x.ai/python-sdk/)。该 SDK 提供了一种新的编程范式，可以优雅地实现复杂的提示词技术。所有 Python 函数都在一个隐式上下文（即一个 token 序列）中执行。你可以用 `prompt()` 函数手动向上下文添加 token，也可以用 `sample()` 函数让我们的模型基于上下文生成 token。

代码通过浏览器内的 Python 解释器在本地执行，该解释器运行在独立的 web worker 中。多个 web worker 可以同时运行，这意味着你可以并行执行许多提示词。

![PromptIDE 中的采样概率](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreenshot_42_completion.7528a460.webp&w=3840&q=75)

复杂提示词技术可以在同一个程序中使用多个上下文来实现。如果一个函数被 `@prompt_fn` 装饰器标注，它就会在自己全新的上下文中执行。该函数可以独立于其父上下文执行一些操作，然后用 `return` 语句把结果传回调用者。这种编程范式支持带有任意嵌套子上下文的递归式与迭代式提示词。

## 并发

该 SDK 使用 Python 协程，可以并发处理多个被 `@prompt_fn` 标注的 Python 函数。这能显著缩短完成时间——在处理 CSV 文件时尤其明显。

![PromptIDE 中的采样概率](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreenshot_concurrency.11d9e3f1.webp&w=3840&q=75)

## 用户输入

提示词可以通过 `user_input()` 函数实现交互——它会阻塞执行，直到用户在 UI 的文本框中输入一个字符串。`user_input()` 函数返回用户输入的字符串，随后例如可以通过 `prompt()` 函数将其加入上下文。借助这些 API，只需四行代码就能实现一个聊天机器人：

python

```
await prompt(PREAMBLE)
while text := await user_input("Write a message"):
    await prompt(f"<|separator|>\n\nHuman: {text}<|separator|>\n\nAssistant:")
    await sample(max_len=1024, stop_tokens=["<|separator|>"], return_attention=True)
```

## 文件

开发者可以向 PromptIDE 上传小文件（每个文件最大 5 MiB，总计最多 50 MiB），并在提示词中使用上传的文件。`read_file()` 函数以字节数组的形式返回任何已上传的文件。结合上面提到的并发特性，可以实现批量处理提示词，在多种问题上评估某一种提示词技术。下面的截图展示了一个计算 MMLU 评测分数的提示词。

![PromptIDE 中的采样概率](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreenshot_mmlu2.4f93c032.webp&w=3840&q=75)

# 分析

在执行提示词的过程中，用户会看到详细的逐 token 分析，帮助他们更好地理解模型的输出。补全窗口会显示上下文的精确分词结果以及每个 token 的数字标识符。点击某个 token 时，用户还能看到应用 top-P 阈值后的 top-K token，以及该 token 处的聚合注意力掩码。

![PromptIDE 中的采样概率](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreenshot_42_completion.7528a460.webp&w=3840&q=75)
![PromptIDE 中的采样概率](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreenshot_42_token.6f1a00f3.webp&w=3840&q=75)

使用 `user_input()` 函数时，提示词运行期间窗口中会出现一个文本框，供用户输入回复。下面的截图展示了执行上述聊天机器人代码片段的结果。

![PromptIDE 中的采样概率](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreenshot_chat_completion.115e94dc.webp&w=3840&q=75)

最后，在不需要 token 可视化功能时，上下文也可以渲染为 markdown 以提升可读性。

![PromptIDE 中的采样概率](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreenshot_completion_markdown.fcfdaf7c.webp&w=3840&q=75)

在以下平台试用 Grok

[Web](https://grok.com)

[iOS](https://apps.apple.com/app/grok/id6670324846)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[X 上的 Grok](https://x.com/i/grok)

产品

[Grok](/grok)

[API](/api)

公司

[公司介绍](/company)

[招聘](/careers)

[联系我们](/contact)

[新闻](/news)

资源

[状态](https://status.x.ai)

[隐私政策](/privacy-policy)

[安全](/security)

[法律](/legal)
