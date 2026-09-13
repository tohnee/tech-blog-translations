---
title: "在 Gemini 应用中获得最佳图像生成与编辑效果的技巧"
title_en: "Tips for getting the best image generation and editing in the Gemini app"
source: https://blog.google/products-and-platforms/products/gemini/image-generation-prompting-tips/
site: gemini
date: 2025-08-26
crawled: 2026-09-13
translated: 2026-09-13
---

# 在 Gemini 应用中获得最佳图像生成与编辑效果的技巧

> 原文：[Tips for getting the best image generation and editing in the Gemini app](https://blog.google/products-and-platforms/products/gemini/image-generation-prompting-tips/) · Google

今天早些时候，我们发布了一款最先进的图像生成与编辑模型，现已在 [Gemini 应用](http://gemini.google.com)、[AI Studio](http://aistudio.google.com/) 和 [Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/gemini-2-5-flash-image-on-vertex-ai) 中可用。这次更新在角色一致性、精确的对话式编辑，以及将多张照片合成为全新作品的能力方面带来了重大进步。为了帮助你充分利用这次更新，以下是一些在 Gemini 中为图像生成与编辑撰写更有效提示词的技巧。

## Gemini 图像生成的关键能力

在开始之前，先熟悉一下 Gemini 有哪些改进，以便思考可以尝试哪些使用场景：

1. **一致的角色设计。** 在多次生成和编辑中保持角色或物体的外观。
2. **创意构图。** 把来自多个概念的迥异元素、主体和风格融合成一张统一的图像。
3. **局部编辑。** 用简单的语言对图像的特定部分进行精确编辑。
4. **设计与外观迁移。** 把一种风格、纹理或设计从一个概念应用到另一个概念。
5. **逻辑与推理。** 运用对现实世界的理解来生成复杂场景，或预测序列中的下一步。

## 构建有效提示词的 6 个要素

用简单的一两句话输入，你也能从 Gemini 获得不错的结果。不过，要取得最佳效果并解锁更细腻的创意控制，请考虑在提示词中加入以下要素：

- **主体（Subject）：** 图像中是谁或什么？要具体。（例如，*a stoic robot barista with glowing blue optics*（一台眼神发出蓝光、表情坚毅的机器人咖啡师）；*a fluffy calico cat wearing a tiny wizard hat*（一只戴着小小巫师帽的蓬松三花猫））。
- **构图（Composition）：** 镜头如何取景？（例如，*extreme close-up*（大特写）、*wide shot*（远景）、*low angle shot*（低角度镜头）、*portrait*（人像））。
- **动作（Action）：** 正在发生什么？（例如，*brewing a cup of coffee*（冲泡一杯咖啡）、*casting a magical spell*（施展魔法）、*mid-stride running through a field*（奔跑着穿越田野））。
- **场景（Location）：** 场景发生在哪里？（例如，*a futuristic cafe on Mars*（火星上的一家未来主义咖啡馆）、*a cluttered alchemist's library*（一间凌乱的炼金术士书房）、*a sun-drenched meadow at golden hour*（黄金时刻阳光普照的草地））。
- **风格（Style）：** 整体美学是什么？（例如，*3D animation*（3D 动画）、*film noir*（黑色电影）、*watercolor painting*（水彩画）、*photorealistic*（照片级写实）、*1990s product photography*（90 年代产品摄影））。
- **编辑指令（Editing Instructions）：** 修改现有图像时，指令要直接、具体。（例如，*change the man's tie to green*（把男士的领带改成绿色）、*remove the car in the background*（去掉背景中的汽车））。

## 提示词示例：创意技法集锦

不同的提示词策略可以解锁一切，从照片级的编辑到奇幻的新世界。以下是五种可尝试的技法，每种都配有关键示例。

### 1. 保持角色外观一致。

Gemini 可以在不同姿势、光照和环境下保持人物或角色的容貌一致，甚至可以把同一角色应用到新的风格和表面上。以下示例展示了如何在同一次会话的多个提示词中使用同一个角色：

- **Prompt 1:** A whimsical illustration of a tiny, glowing mushroom sprite. The sprite has a large, bioluminescent mushroom cap for a hat, wide, curious eyes, and a body made of woven vines.
- **Prompt 2 (in the same conversation):** Now, show the same sprite riding on the back of a friendly, moss-covered snail through a sunny meadow full of colorful wildflowers.

![并排的奇幻插画：一个戴着蘑菇帽的小精灵般的小生物。左边，它漂浮在幽暗多雾的森林中。右边，它骑着一只微笑的蜗牛穿越阳光下的野花田。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/pixie.width-1200.format-webp.webp)

通过在第一个提示词中用具体细节定义一个清晰的角色，你可以用后续提示词把这个*同一角色*放进全新的情境。在这里，Gemini 保留了角色的关键特征，如五官、独特外形和服装。

### 2. 精准进行定向变换。

借助更新的图像编辑能力，你可以对照片进行快速、高度精确的编辑。从产品效果图到完善个人照片，这都再合适不过。示例如下：

- **Prompt 1:** A high-quality photo of a modern, minimalist living room with a grey sofa, a light wood coffee table, and a large potted plant.
- **Prompt 2 (editing):** Change the sofa's color to a deep navy blue.
- **Prompt 3 (editing):** Now, add a stack of three books to the coffee table.

![三张并排的客厅图片展示了不同的室内设计选择。第一张照片是一张灰色沙发，第二张是深蓝色沙发，第三张是同一张蓝色沙发，咖啡桌上多了一摞书。三张图构成一组对比。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/livingroom.width-1200.format-webp.webp)

这展示了 Gemini 在局部编辑方面的实力。通过直接、对话式的指令，你可以修改图像中的特定元素，而无需复杂的软件，也无需重新生成整个场景。

### 3. 用创意构图融合概念。

尝试把两个或更多的想法融合成一张令人惊艳的图像。让 Gemini 生成两张图像，然后用富有想象力的方式把它们的主体和环境组合起来：

- **Prompt 1:** Generate a photorealistic picture of an astronaut in a helmet and full suit.
- **Prompt 2:** A picture of an overgrown basketball court in the rainforest.
- **Prompt 3 (upload both and combine):** Show the astronaut dunking a basketball in this court.

![三格连图：一名身着宇航服的宇航员在火星上，一片被热带雨林吞噬的废弃篮球场，以及这名宇航员在那片球场上扣篮。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/astronaut.width-1200.format-webp.webp)

### 4. 适配并应用新风格。

通过应用新的风格、配色或纹理，彻底改变图像的氛围与美学，同时保持原始主体不变。

- **Prompt 1:** A photorealistic image of a classic motorcycle parked on a city street.
- **Prompt 2 (editing):** Apply the style of an architectural drawing to this image.

![并排对比：一张停放的摩托车的精细照片，以及同一场景的黑白线条画。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/bike.width-1200.format-webp.webp)

通过"风格迁移"，Gemini 理解核心主体（摩托车）及其形态，然后完全按照要求的艺术风格重新渲染它。这可以用于设计灵感、艺术探索等更多用途。

### 5. 用逻辑与推理完成复杂生成。

给 Gemini 一个简单的概念，让它的推理能力把细节展开。这对于创建需要理解现实世界关系或过程的内容非常有用。

- **Prompt 1:** Generate an image of a person standing holding a 3 tiered cake.
- **Prompt 2 (in the same session):** Generate an image showing what would happen if they tripped.

![两格图：一位厨师捧着一个完好的三层蛋糕；随后是同一蛋糕摔得四分五裂、厨师震惊地看着的第二张图。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/chef.width-1200.format-webp.webp)

模型可以运用其逻辑与推理能力预测接下来会发生什么。它理解第一张图像的上下文和物理规律——一个人小心翼翼地端着蛋糕——进而可以模拟摔倒之类的动作可能带来的合理后果，生成一张动态且贴合情境的新图像。

## 关于当前局限的说明

在我们持续开发和微调模型的同时，仍有一些方面需要改进：

- **风格化：** 模型的风格化能力虽然强大，但有时会不稳定或产生意外的结果。
- **文字渲染：** 模型偶尔可能拼错单词，或在复杂排版上表现不佳。
- **角色特征：** 尽管模型在角色一致性上表现出色，但它并非总能做到完美。我们正努力让这种一致性更加可靠。
- **设置和保持宽高比：** 模型在保持宽高比方面存在困难——虽然你可以在提示词中指定期望的尺寸，但输出结果并不总能满足你的要求。

我们正在积极改进这些方面，并感谢你在我们共同打造下一代图像工具的过程中展现的创造力。

创意果实已经成熟，等你采摘——我们迫不及待想看到你的创作！

*特别感谢 Greenfield 团队的资深生成工程师们做出的创意贡献。*
