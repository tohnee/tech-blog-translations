---
title: "在开发者控制台中评估提示"
title_en: "Evaluate prompts in the developer console"
source: https://claude.com/blog/evaluate-prompts/
crawled: 2026-09-14
translated: 2026-09-14
---

# 在开发者控制台中评估提示

> 原文：[Evaluate prompts in the developer console](https://claude.com/blog/evaluate-prompts/) · Claude 博客

构建 AI 驱动的应用时，提示（prompt）质量会显著影响最终结果。但编写高质量提示颇具挑战，既需要深入了解应用的需求，也需要具备大语言模型方面的专业知识。为了加快开发速度、改善效果，我们对这一流程进行了简化，让用户更轻松地产出高质量提示。

现在，你可以在 Anthropic Console 中生成、测试和评估你的提示。我们新增了多项功能，包括自动生成测试用例和比较输出结果的能力，让你能够借助 Claude 为自己的需求生成最优质的响应。

### 生成提示

写好一个提示可以很简单：只需向 Claude 描述一个任务。Console 提供了一个由 Claude 3.5 Sonnet 驱动的[内置提示生成器](https://www.anthropic.com/news/prompt-generator)，你可以描述自己的任务（例如「对收到的客户支持请求进行分类分派」），让 Claude 为你生成一个高质量的提示。

你可以使用 Claude 全新的测试用例生成功能为提示生成输入变量——例如一条客户支持消息——然后运行提示，查看 Claude 的响应。你也可以手动输入测试用例。

### 生成测试套件

在部署到生产环境之前，用一系列真实世界中的输入来测试提示，有助于你建立对提示质量的信心。借助全新的 Evaluate 功能，你可以直接在 Console 中完成这一切，而不必在电子表格或代码里手动管理测试。

你可以手动添加测试用例，或从 CSV 导入，也可以使用「Generate Test Case」功能让 Claude 自动生成测试用例。按需修改测试用例，然后一键运行全部测试用例。你还可以查看并调整 Claude 对每个变量生成要求的理解，从而对 Claude 生成的测试用例进行更细粒度的控制。

### 评估模型响应并迭代提示

现在，打磨提示所需的步骤更少了：你可以创建提示的新版本并重新运行测试套件，快速迭代、改进结果。我们还新增了将两个或多个提示的输出并排比较的能力。

你甚至可以让领域专家按 5 分制为响应质量打分，以查看你所做的改动是否提升了响应质量。这两项功能都让提升模型性能变得更快、更易上手。

### 开始使用

测试用例生成和输出比较功能现已面向 Anthropic Console 的所有用户开放。想进一步了解如何使用 Claude 生成和评估提示，请查阅我们的[文档](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)。

FAQ（常见问题）
