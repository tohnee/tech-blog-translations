---
title: "在 Opal 中构建动态智能体工作流"
title_en: "Build dynamic agentic workflows in Opal"
source: https://blog.google/innovation-and-ai/models-and-research/google-labs/opal-agent/
site: google-blog
date: 2026-02-24
crawled: 2026-09-13
translated: 2026-09-13
---

# 在 Opal 中构建动态智能体工作流

> 原文：[Build dynamic agentic workflows in Opal](https://blog.google/innovation-and-ai/models-and-research/google-labs/opal-agent/) · Google

今天，我们将 [Opal](https://opal.google/) 的工作流从静态模型调用升级为智能体智能。你不再需要手动挑选模型——现在，你可以在「generate」步骤中选择一个智能体（agent）。这个智能体步骤会根据你的目标主动确定最佳路径，触发合适的工具和模型（比如用 Web Search 做调研，或用 Veo 生成视频），以更少的手动配置自动完成复杂任务。

![之前](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Before.width-1200.format-webp.webp)

此前，创建一个[故事书 Opal](https://opal.google/app/11QKom2khoCwTKZje4bqOdDD8PIgmp3oP) 需要你预先定义页数和用户问题。现在，我们可以创建一个 [Visual Storyteller Opal](https://opal.google/app/1M3Pt6yeU2exdRzGlRDmLKKqz7O5gjJsi)，由智能体步骤自主决定需要哪些细节，并建议情节点，帮助你引导故事的走向。这标志着从僵化格式向动态、独特叙事的转变——由实时的创意决策塑造。

![之后](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/After.width-1200.format-webp.webp)

## 从静态到交互式体验

以一个室内设计 Opal 为例。在智能体步骤出现之前，[Interior Design Opal](https://opal.google/app/1S5oHfPwMNd2CS75Y-LcbfuR8hMJHw-lS) 感觉像一个简单的单向流程：上传一张图片，输入你的风格，然后收到一张重新设计的空间图像。有了新的智能体步骤，你升级后的 [Room Styler Opal](https://opal.google/app/1Gg7oEWui9xMpBvinD7AcVzWRthRPW1-m) 开始变得可交互，更像一位与你协作的设计伙伴。

上传一张空客厅的照片，描述你想要的世纪中期现代主义（mid-century modern）构想。智能体会生成一个带有时代特色装饰与配色方案的初始概念。如果不太对味，你可以对具体元素提供反馈。通过这样的对话式迭代，智能体会不断加深对你审美的理解，甚至可以研究小众的设计子风格，创造出真正独属于你的重新设计图像，而不是千篇一律的样板间模板。

![室内设计 Opal](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/interior_design_opal.gif)

Opal 现在之所以能创建这些交互式体验，是因为智能体理解你的目标，思考完成任务的最佳方式，在需要你的输入时主动询问，并调集最合适的模型和工具来完成工作。

## 让你的 Opal 智能体更强大的新工具

- **记忆（Memory）**：无论是用户的名字、你的风格偏好，还是一份不断更新的购物清单，你的 Opal 现在可以跨会话记住信息。这让你的 Opal 越用越聪明，越用越有个人色彩。在这个 [Video Hooks Brainstormer Opal](https://opal.google/app/1g6xmNVFNwOQXTT1qdUcaruhNdS2iUFYs) 中，智能体步骤会将用户的品牌标识与偏好存入记忆，让你无需重复偏好，就能立即生成量身定制的视频创意。

![Opal 智能体使用记忆](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Opal_Agent_-_Using_Memory.width-1200.format-webp.webp)

- **动态路由（Dynamic routing）**：通过基于自定义逻辑定义智能体可以遵循的多条路径，全面掌控你的工作流。只需描述你的条件，一旦条件满足，智能体就会智能地切换到正确的步骤。在 [Executive Briefing Opal](https://opal.google/app/1s0g2KqYyu82TFampYJ3iEp6014X78QVa) 中，智能体步骤会根据你会见的是老客户还是新客户来定制简报：它会搜索网络了解新客户的背景，或审阅内部会议记录以提供相关背景信息。

![Opal 智能体动态路由](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Go_to_updated_yLmPAPW.width-1200.format-webp.webp)

- **交互式对话（Interactive chat）**：有时 AI 智能体需要提出后续问题。智能体步骤现在可以主动与用户发起对话，收集缺失的信息，或在进入计划的下一阶段前提供选项。以 [Room Styler Opal](https://opal.google/app/1Gg7oEWui9xMpBvinD7AcVzWRthRPW1-m) 为例，如果用户一开始没有给出足够细节，Opal 会继续提问或展示示例。

![Opal 智能体交互式对话](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Opal_Agent_-_Interactive_Chat.width-1200.format-webp.webp)

## 在 Opal 中构建的更多方式

我们相信，这种方式为你带来两全其美的体验：既有 AI 智能体为你的目标工作的强大能力，又有分步工作流的掌控力——随时可以自定义和打磨。

我们在保持 Opal 简单易用的同时，让它变得更加强大。新用户会发现 Opal「开箱即用」，因为 generate 步骤中的智能体足够聪明，能够自我纠正、记忆和优化。对于我们的高阶用户和构建者，标准的固定步骤随时可用，满足高精度原型设计或严格逻辑的需要。通过弥合自动化与控制之间的鸿沟，我们正在拓展你能构建的边界。我们迫不及待想看到你的新智能体驱动的 Opal 大显身手！
