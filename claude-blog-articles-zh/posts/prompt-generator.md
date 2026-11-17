---
title: "在开发者控制台中生成更好的提示词"
title_en: "Generate better prompts in the developer console"
date: 2024-05-20
source: https://claude.com/resources/articles/prompt-generator
crawled: 2026-11-17
translated: 2026-11-17
---

# 在开发者控制台中生成更好的提示词

> 原文：[Generate better prompts in the developer console](https://claude.com/resources/articles/prompt-generator) · Claude 博客

Claude 现在可以生成可直接投产的提示词模板，帮助开发者更快地创建有效的提示词。

你现在可以在 Anthropic Console 中生成可直接投产的提示词模板。描述你想达成的目标，Claude 就会运用思维链推理等提示词工程技术，创建出有效、精确且可靠的提示词。

该功能旨在帮助刚接触提示词工程的用户，同时也为经验丰富的提示词工程师节省时间。向提示词生成器提供关于任务和期望输出格式的详细信息，效果最佳。

虽然生成的提示词并不总能产生完美结果，但它们往往优于提示词工程新手手写的提示词。生成的提示词模板也可以编辑，让你快速微调以达到最佳表现。

## 提示词最佳实践

该新功能生成的提示词模板运用了我们的许多[提示词工程最佳实践](https://docs.anthropic.com/en/docs/prompt-engineering)。其中一项是[角色设定](https://docs.anthropic.com/en/docs/give-claude-a-role)（role setting），鼓励 Claude 扮演所选任务专家的角色。在我们的内容审核示例中，角色设定是这样的：

```
You will be acting as a content moderator to classify chat transcripts as either approved or rejected based on a provided content moderation policy.
```

> 【译者注：本文中的提示词示例均为可直接复制使用的原文，保留英文不作翻译。】

另一项实践是[思维链](https://docs.anthropic.com/en/docs/let-claude-think)（chain of thought）推理，即给 Claude 时间和空间在回答前整理思路。这能让复杂查询得到更周全、更有条理的回答。当我们要求为「基于客户过往交易给出产品推荐」生成提示词时，这一实践是这样实现的：

```
In a <scratchpad>, brainstorm 3 different product recommendations you could make to this customer based on their transaction history. For each potential recommendation, provide a brief rationale explaining why you think it would be a good fit for this customer.
```

此外，模板通常会把「变量」——即可插入自定义数据的输入字段——放在 [XML 标签](https://docs.anthropic.com/en/docs/use-xml-tags)之间。这遵循了另一项关键最佳实践：通过清晰的结构划分提示词的不同部分。当我们要求生成一个把代码翻译成 Python 的提示词时，可以看到更长、更含糊的 `{{CODE}}` 变量被 XML 标签标记，而简单的 `{{LANGUAGE}}` 变量则内联放置。

```
Your task is to translate a piece of code from another programming language into Python.

Here is the code to translate:

<code>
{{CODE}}
</code>

The code is written in {{LANGUAGE}}.
```

在某些情况下，你会看到 Claude 写出[示例输入和输出](https://docs.anthropic.com/en/docs/use-examples)，为自己明确它认为你想要的答案类型。你可以编辑这些示例，使其符合你期望的输出格式。

## 幕后机制

提示词生成器基于一个很长的提示词，而这个提示词本身就运用了许多前面提到的技术。

* 它包含大量任务描述与提示词模板的示例，向 Claude 展示如何从任务描述走到提示词模板。
* 它鼓励 Claude 在写出模板之前先规划模板的结构，让 Claude 有时间整理思路。
* 它有一个由 XML 标签构成的坚实「骨架」，标记每个部分的开始与结束，以提升可读性。

你可以在这个 [Colab notebook](https://colab.research.google.com/drive/1SoAajN8CBYTl79VyTwxtxncfCWlHlyy9#scrollTo=NTOiFKNxqoq2) 中查看完整提示词。

## 把提示词模板当作评估工具

你从提示词生成器获得的模板中的变量将采用 [handlebars](https://handlebarsjs.com/) 记法，如前面的内容审核示例所示：

> 【译者注：原文此处嵌入的示例代码块未能正常渲染，页面上只剩组件报错信息。按上下文，该代码块展示的是内容审核模板中 handlebars 变量（形如 `{{VARIABLE}}`）的用法。】

在这个示例中，你随后可以上传你的内容政策以及一系列不同的聊天记录，观察 Claude 的表现。这一过程让你能确保应用在各种情境下都能恰当回应。

## 客户聚焦：ZoomInfo

市场拓展（go-to-market）平台 ZoomInfo 使用 Claude 提供可执行的建议，为客户创造价值。他们使用提示词生成功能，大幅缩短了构建 RAG 应用 MVP 所需的时间，同时提升了输出质量。

「Anthropic 新的提示词生成器功能让我们能更快达到可投产的输出。它指出了我此前没有使用的一些提升表现的技术，并显著减少了我们调优应用的时间，」ZoomInfo 首席数据科学家 Spencer Fox 表示。「我们构建了一个新的 RAG 应用，仅用几天就达到 MVP，把细化提示词所需的时间减少了 80%。」

## 开始使用

要开始用 Claude 构建可投产的提示词，请访问 [Anthropic API](https://console.anthropic.com/)。
