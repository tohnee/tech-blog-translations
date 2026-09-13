---
title: "Whisk：用图像与 AI 将想法可视化并进行混搭再创作"
title_en: "Whisk: Visualize and remix ideas using images and AI"
source: https://blog.google/innovation-and-ai/models-and-research/google-labs/whisk/
site: google-blog
date: 2024-12-16
crawled: 2026-09-13
translated: 2026-09-13
---

# Whisk：用图像与 AI 将想法可视化并进行混搭再创作

> 原文：[Whisk: Visualize and remix ideas using images and AI](https://blog.google/innovation-and-ai/models-and-research/google-labs/whisk/) · Google

今天，我们在美国推出我们在生成式 AI 领域的最新实验：[Whisk](http://labs.google/whisk)。Whisk 不再需要冗长详细的文本提示词来生成图像，而是让你用图像作为提示词。只需拖入图片，就能开始创作。

Whisk 允许你为主体输入一张图像，为场景输入一张图像，再为风格输入另一张图像。然后，你可以将它们混搭再创作，生成独一无二的作品——从数字毛绒玩偶到珐琅徽章或贴纸，皆有可能。

![这张图片以明亮的黄色为背景，展示了 Whisk 的一个工作示例。右侧是一幅大型精细的插画：一条奇幻的鱼，背上建着一座城市；左侧较小的图片是用于生成它的输入图像——一艘潜水艇、一座漂浮的岛屿和一处风景如画的山川，分别是用于生成最终结果的主图（subject）、场景（scene）和风格（style）图像。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Carousel_-_1.width-100.format-webp.webp)

Whisk - 奇幻之鱼 - 生成图像示例

![这张图片以明亮的黄色为背景，展示了 Whisk 工作方式的第二个示例。它呈现了一幅趣味十足的插画：一头海象身穿草莓图案的泳衣、头戴花冠。左侧显示了输入图像：作为主体的海象、作为场景的花田，以及作为风格的卡通云朵图案。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Carousel_-_2.width-100.format-webp.webp)

Whisk - 趣味海象 - 生成图像示例

![这张图片以明亮的黄色为背景，展示了 Whisk 如何为珐琅徽章生成图像。画面主体是一枚撒着糖屑的彩色糖霜甜甜圈。左侧是一张糖霜甜甜圈的写实照片，旁边是一个金属质感的服务员剪影，它们分别作为最终珐琅徽章生成的主体和风格。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Carousel_-_3.width-100.format-webp.webp)

Whisk - 糖霜甜甜圈配糖屑 - 生成珐琅徽章示例

![这张图片以明亮的黄色为背景，展示了一只长着犄角的奇幻猫。它有着闪亮的紫色调皮毛和醒目的绿色眼睛。这只生物正卧在水面上的一片大睡莲叶上，背景中还有其他睡莲叶。三张图像缩略图是所用的图像输入：一只长着犄角的闪亮猫咪作为主体输入图像，一幅有睡莲的自然场景和一幅有树木与云朵的风景作为风格。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Carousel_-_4.width-100.format-webp.webp)

Whisk - 长犄角的奇幻猫 - 生成图像示例

在幕后，Gemini 模型会自动为你的图像撰写详细的描述文字，然后将这些描述输入 Google 最新的图像生成模型 [Imagen 3](https://blog.google/technology/google-labs/video-image-generation-update-december-2024)。这一过程捕捉的是你主体的*神韵*，而不是精确复刻。这样，你就能轻松地以全新的方式对主体、场景和风格进行混搭再创作。

由于 Whisk 只从你的图像中提取少数关键特征，它生成的图像可能会与你的预期有所不同。例如，生成的主体可能有着不同的身高、体重、发型或肤色。我们理解这些特征对你的项目可能至关重要，而 Whisk 可能会有偏差，因此我们允许你随时查看并编辑底层提示词。

在对艺术家和创意工作者的早期测试中，人们将 Whisk 描述为一种新型创意工具——而非传统的图像编辑器。我们打造它是为了快速进行视觉探索，而不是进行像素级的精确编辑。它的意义在于以新颖而富有创意的方式探索想法，让你快速尝试数十种方案，并下载你喜爱的那些。

如果你位于美国，现在就可以在 [labs.google/whisk](http://labs.google/whisk) 试用，并告诉我们你的想法。

[Google Labs](https://labs.google/) 是我们用 Gemini、Imagen 和 Veo 等最新生成式 AI 模型烹饪各种实验的地方。我们的目标是在共同塑造技术的过程中，收集针对新产品和新功能的反馈。你可以订阅[我们的新闻通讯](https://docs.google.com/forms/d/e/1FAIpQLSeb9kO7BsAN4ciqPNGuycoWGtsYXbppm08IEvksGbabBUWk9Q/viewform?resourcekey=0-DESTeP8_FmaUC2WrHt_YJA)，并在 [X](https://x.com/googlelabs)、[Reddit](https://www.reddit.com/r/labsdotgoogle/) 和 [Discord](http://discord.gg/googlelabs) 上关注 Google Labs，随时了解 Whisk 及其他实验的最新动态。
