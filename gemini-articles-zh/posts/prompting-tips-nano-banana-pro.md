---
title: "充分利用 Nano Banana Pro 的 7 个技巧"
title_en: "7 tips to get the most out of Nano Banana Pro"
source: https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/
site: gemini
date: 2025-11-20
crawled: 2026-09-13
translated: 2026-09-13
---

# 充分利用 Nano Banana Pro 的 7 个技巧

> 原文：[7 tips to get the most out of Nano Banana Pro](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/) · Google

我们对 Nano Banana 进行了一次大规模升级。基于 Gemini 3 构建的 Nano Banana Pro 是我们迄今最先进的图像模型，随时准备弥合想象力与专业执行之间的差距。

它现已在 Gemini 应用中可用，并开始在 AI Studio、Vertex 及更多平台推送，具备多语言的最先进文本渲染能力，以及高级控制功能——比如最多可将 14 张图像输入一个构图（因平台而异）。

要开始使用这款强大的新模型，请查看我们的[发布文章](https://blog.google/technology/ai/nano-banana-pro)以及下面这份关于撰写有效专业提示词的指南。

---

## 确立愿景：故事、主体与风格

要获得最佳结果并对创作拥有更细腻的掌控，请在提示词中包含以下要素：

- **主体：** 图像里是谁或是什么？要具体。（例如：一个眼神发着蓝光、神情坚毅的机器人咖啡师；一只戴着小小巫师帽、毛茸茸的三花猫）。
- **构图：** 镜头如何取景？（例如：极特写、远景、低角度镜头、肖像）。
- **动作：** 正在发生什么？（例如：冲泡一杯咖啡、施展魔法、奔跑着穿过一片田野）。
- **地点：** 场景发生在哪里？（例如：火星上的一家未来主义咖啡馆、一间杂乱的炼金术士书房、黄金时刻洒满阳光的草甸）。
- **风格：** 整体美学是什么？（例如：3D 动画、黑色电影、水彩画、照片级写实、1990 年代产品摄影）。
- **编辑指令：** 若要修改现有图像，要直接而具体。（例如：把男士的领带改成绿色，去掉背景中的汽车）

## 打磨细节：相机、光线与格式

简单提示词依然有效，但要达到专业效果，就需要更具体的指令。撰写提示词时，请超越基础要素，考虑这些进阶元素：

- **构图与长宽比：** 定义画布。（例如：「一张 9:16 的竖版海报」「一个电影感的 21:9 宽镜头」）。
- **相机与光线细节：** 像电影摄影师一样调度镜头。（例如：「浅景深（f/1.8）的低角度镜头」「黄金时刻的逆光拉出长长的影子」「带有柔和青色调的电影级调色」）。
- **明确的文本整合：** 清楚说明应出现什么文字、以什么样式呈现。（例如：「标题『URBAN EXPLORER』以粗体白色无衬线字体呈现在顶部」）。
- **事实性约束（用于图表）：** 明确对准确性的要求，并确保你的输入本身符合事实（例如：「一张科学上准确的剖面图」「确保维多利亚时代的历史准确性」）。
- **参考输入：** 使用上传的图像时，清楚界定每张图的角色。（例如：「用图像 A 定角色姿势，图像 B 定艺术风格，图像 C 定背景环境」）。

---

## 提示词实例：创意技巧展示

不同的提示词策略可以帮你创作一切——从照片级写实的编辑，到奇幻的全新世界。以下是一些值得尝试的技巧：

**1. 生成文本渲染出色的视觉作品：** 锐利、清晰可读的文字能帮你创作冲击力十足的海报、精细的图表，乃至细致的产品样机。

**2. 借助真实世界知识进行创作：** 基于 [Gemini 3 Pro](https://blog.google/products/gemini/gemini-3/) 构建，Nano Banana 运用 Gemini 3 的真实世界知识与深度推理能力，提供精准、细致、丰富的图像结果。

**3. 翻译并本地化你的创意：** 生成本地化文本，或翻译图像内的文字。看看产品在[多种语言](http://deepmind.google/models/gemini-image/pro)下会是什么样子，为国际市场做好准备，并为不同地区创作海报和信息图。

![关于宇航员的分镜脚本](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Astronaut.width-100.format-webp.webp)

图注：一幅黑白分镜草图，展示了一个电影场景的定场镜头、中景、特写和主观视角（POV）镜头。

Prompt: Create a storyboard for this scene

![Woodchuck AI 生成图像](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Text_Rendering_2.width-100.format-webp.webp)

Prompt: Create an image showing the phrase "How much wood would a woodchuck chuck if a woodchuck could chuck wood" made out of wood chucked by a woodchuck.

![豆蔻奶茶制作信息图](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/World_Knowledge_Elaichi_Chai.width-100.format-webp.webp)

Prompt: Create an infographic that shows how to make elaichi chai

![黄蓝罐子上的文字被翻译成韩文](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/NanoBanana_TranslateCans_8COQLPB.width-100.format-webp.webp)

Prompt: translate all the English text on the three yellow and blue cans into Korean, while keeping everything else the same

**4. 使用影棚级质量的控制式编辑：** 获得丰富的控制选项，达成专业级效果。可以直接左右光线和相机设置，如角度、对焦、调色等等。

**5. 精准调整尺寸：** 尝试不同的长宽比，在各类产品中以 1K、2K 或 4K 分辨率生成清晰的视觉作品。

**6. 融合图像并保持多个角色的一致性：** 保持多个角色的一致性与相似度，即使他们同框出现在群像中。最多可将 6 到 14 张（输入数量因平台而异）毫不相关的图像融合在一起，创造出全新的内容。

**7. 创建并维护你的品牌观感：** 渲染并应用具有一致品牌风格的设计，轻松呈现各种概念。可将图案、标志和 artwork 无缝地贴合到 3D 物体和表面上——从服装到包装——同时保留自然的光影与质感。

![白天和夜晚的狐狸](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WM-Fox.width-100.format-webp.webp)

Prompt: Turn this scene into nighttime

![焦点在女孩身上，然后焦点转到花朵上](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WM---Flower-Girl.width-100.format-webp.webp)

Prompt: Focus on the flowers

![一个周身环绕羽毛的人物，呈现多种长宽比](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WM-Aspect-Ratio.width-100.format-webp.webp)

通过调整长宽比，为一系列平台改变一张图像的观感。

![由多个元素合成的时尚图像](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Multi-Asset-Fashion.width-100.format-webp.webp)

Prompt: Combine these images into one appropriately arranged cinematic image in 16:9 format and change the dress on the mannequin to the dress in the image.

![一个 logo 输入，借助 Nano Banana Pro 延伸出设计中的多种应用](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/nanowave.width-100.format-webp.webp)

Prompt 1: Create a smooth logo in a graphic style is a vibrant and playful form of typographic illustration, deeply rooted in the retro aesthetics of the 1960s and 1970s loosely based on the sketch Its defining feature is a groovy, psychedelic-inspired typeface characterized by soft, rounded, and fluid letterforms. Don't exactly follow the sketch, get inspired from it. The letters are skillfully distorted, stretched, and compressed, abandoning rigid structure to flow together and form a cohesive, recognizable shape.
This technique, known as a calligram, masterfully merges text and image, where the word's form visually embodies its meaning. The word "WAVE" is artfully arranged into the fluid silhouette of a wave. The design is a clever visual pun, making the message instantly accessible and memorable.
The color palette reinforces the vintage feel, employing a simple two-toned scheme with warm, often muted or earthy colors light blue background and deep blue logo. This choice enhances the nostalgic charm of the artwork. The overall effect is one of whimsical nostalgia and clever graphic design. It’s a bold yet approachable style that communicates a simple, positive message through the seamless integration of shape and word, creating an immediate and delightful visual impact.

Prompt 2: Now create identity system one by one, use 10 high quality mockups with variety of relevant products, ads, billboards, bus stop, etc. generate one at a time, 16:9 each

## 关于当前局限的说明

在我们持续开发并微调模型的过程中，仍有一些有待改进之处：

- **视觉与文本保真度：** 渲染小号文字、精细细节以及生成准确拼写可能并不完美。
- **数据与事实准确性：** 请务必核实图表、信息图等数据驱动视觉作品的事实准确性。
- **翻译与本地化：** 多语言文本生成可能出现语法错误或遗漏特定的文化细微之处。
- **复杂编辑与图像融合：** 融合或光线调整等高级编辑任务有时会产生不自然的瑕疵。
- **角色特征：** 虽然通常可靠，但角色在多次编辑间的一致性可能有波动。

我们正在积极改进这些方面，也感谢你的创造力——让我们共同打造下一代图像工具。
