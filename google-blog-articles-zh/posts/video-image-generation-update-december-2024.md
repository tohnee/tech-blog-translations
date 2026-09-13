---
title: "Veo 2 与 Imagen 3：业界最先进的视频生成与图像生成"
title_en: "State-of-the-art video and image generation with Veo 2 and Imagen 3"
source: https://blog.google/innovation-and-ai/models-and-research/google-labs/video-image-generation-update-december-2024/
site: google-blog
date: 2024-12-16
crawled: 2026-09-13
translated: 2026-09-13
---

# Veo 2 与 Imagen 3：业界最先进的视频生成与图像生成

> 原文：[State-of-the-art video and image generation with Veo 2 and Imagen 3](https://blog.google/innovation-and-ai/models-and-research/google-labs/video-image-generation-update-december-2024/) · Google

[今年早些时候](https://blog.google/technology/ai/google-generative-ai-veo-imagen-3/)，我们推出了视频生成模型 Veo 和最新的图像生成模型 Imagen 3。从那时起，看到人们借助这些模型将自己的创意变为现实，令人兴奋不已：YouTube 创作者正在探索为 YouTube Shorts 制作[视频背景](https://www.youtube.com/watch?v=HO-Z5kO8scA)的创意可能，企业客户正在 [Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/introducing-veo-and-imagen-3-on-vertex-ai) 上增强创意工作流，而创意工作者则在使用 [VideoFX](https://labs.google/fx/tools/video-fx) 和 [ImageFX](https://labs.google/fx/tools/image-fx) 讲述自己的故事。从电影人到企业，我们正与各类合作者一道，持续开发和演进这些技术。

今天，我们推出新的视频模型 Veo 2 以及 Imagen 3 的最新版本，两者都达到了业界最先进的水平。这些模型现已在 VideoFX、ImageFX 以及我们最新的 Labs 实验 [Whisk](https://labs.google/fx/tools/whisk) 中可用。

## Veo 2：业界最先进的视频生成

Veo 2 能够创建覆盖广泛主题和风格、质量惊人的视频。在由人类评审员评判的正面对比中，Veo 2 对比领先模型取得了[业界最先进的结果](https://deepmind.google/technologies/veo/veo-2)。

它对现实世界物理规律以及人类动作与表情的细微之处有了更好的理解，这有助于全面提升其细节表现和真实感。Veo 2 懂得电影摄影的独特语言：让它指定一种类型、指定一种镜头、建议一种电影效果，Veo 2 都能满足——分辨率最高可达 4K，时长可延展至数分钟。要求一个低角度跟拍镜头滑过场景中央，或者一个科学家透过显微镜观察时面部的特写镜头，Veo 2 都能创建出来。在提示词中写上「18mm 镜头」，Veo 2 就知道要打造这种镜头所特有的广角画面；或者写上「浅景深」，它就会虚化背景、聚焦你的主体。

Veo 2 高质量视频生成能力的示例。所有视频均由 Veo 2 生成，未经修改。

Veo 2 高质量视频生成能力的示例。所有视频均由 Veo 2 生成，未经修改。

Veo 2 高质量视频生成能力的示例。所有视频均由 Veo 2 生成，未经修改。

Veo 2 高质量视频生成能力的示例。所有视频均由 Veo 2 生成，未经修改。

Veo 2 高质量视频生成能力的示例。所有视频均由 Veo 2 生成，未经修改。

Veo 2 高质量视频生成能力的示例。所有视频均由 Veo 2 生成，未经修改。

Veo 2 高质量视频生成能力的示例。所有视频均由 Veo 2 生成，未经修改。

视频模型常常会「幻觉」出多余的细节——比如多余的手指或意料之外的物体——而 Veo 2 出现这类问题的频率更低，使输出更加逼真。

我们对安全与负责任开发的承诺贯穿 Veo 2 的设计。我们在扩大 Veo 可用性方面刻意保持审慎，以便在通过 VideoFX、YouTube 和 Vertex AI 逐步推送的过程中，帮助识别、理解和改进模型的质量与安全性。

与我们其余的图像和视频生成模型一样，Veo 2 的输出包含不可见的 SynthID 水印，有助于将其识别为 AI 生成内容，从而降低错误信息和错误归因的可能性。

今天，我们将全新的 Veo 2 能力带入 Google Labs 的视频生成工具 VideoFX，并扩大可以使用它的用户规模。请访问 [Google Labs](https://labs.google/fx/tools/video-fx) 注册候补名单。我们还计划明年将 Veo 2 扩展到 YouTube Shorts 及其他产品。

*注：本文底部可找到所有视频的提示词：科学家*
[1](#footnote-1)
*、卡通角色*
[2](#footnote-2)
*、蜜蜂*
[3](#footnote-3)
*、火烈鸟*
[4](#footnote-4)
*、立方体*
[5](#footnote-5)
*、狗*
[6](#footnote-6)
*、煎饼*
[7](#footnote-7)

## Imagen 3：业界最先进的图像生成

我们还改进了 [Imagen 3](https://deepmind.google/technologies/imagen-3/) 图像生成模型，它现在生成的图像更加明亮、构图更佳。它可以更准确地呈现更多元的艺术风格——从照片级写实主义到印象派，从抽象艺术到动漫。这次升级还能更忠实地遵循提示词，呈现更丰富的细节和纹理。在人类评审员对其输出与领先图像生成模型进行的并排对比中，Imagen 3 取得了[业界最先进的结果](https://deepmind.google/technologies/imagen-3/)。

从今天起，最新的 Imagen 3 模型将在我们来自 Google Labs 的图像生成工具 ImageFX 中向 100 多个国家/地区全球推送。访问 [ImageFX](https://labs.google/fx/tools/image-fx) 即可开始使用。

![一张特写镜头捕捉到冬日仙境的场景——柔软的雪花飘落在积雪覆盖的森林地面上。在一根结霜的松枝后，一只红松鼠端坐着，它亮橙色的皮毛在白色背景中格外醒目。它捧着一颗小榛子。当它享用美餐时，似乎浑然不觉飘落的雪花。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/watermarked_photo_squirrel_snow.width-100.format-webp.webp)

Imagen 3 丰富细节与图像质量构图的示例

![一张极近距离特写：一位手艺人的双手正在转盘上塑造一件泛着微光的陶器。金色的发光能量细丝连接着陶艺师的双手与陶土，随着他们的动作动态旋转。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/watermarked_photo_potter_sparks.width-100.format-webp.webp)

Imagen 3 丰富细节与图像质量构图的示例

![黎明时分一个雾气弥漫的 20 世纪 40 年代欧洲火车站，由繁复的锻铁拱门和蒙着雾气的玻璃窗框起。蒸汽从铁轨上升腾而起，与浓雾融为一体。一对恋人在火车旁深情相拥，身后是昏暗灯笼散发的温暖琥珀色光芒的逆光。驶离的火车隐约可见，红色的尾灯渐渐消失在雾中。女子身穿褪色的红色大衣，紧握着一本小小的皮质日记本；男子则身穿饱经风霜的军装。尘埃微粒在空气中漂浮，被柔和的金色逆光照亮。氛围忧郁而隽永，唤起战争电影中苦乐参半的离别。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/watermarked_photo_train_station.width-100.format-webp.webp)

Imagen 3 丰富细节与图像质量构图的示例

![一位亚洲女性的肖像，背景是霓虹绿灯光，浅景深。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/watermarked_photo_woman_neon_1.width-100.format-webp.webp)

Imagen 3 丰富细节与图像质量构图的示例

![一张特写微距摄影图库照片：一颗草莓被精巧地雕刻成正在飞翔的蜂鸟形状，它正从一朵鲜艳的管状花中吸食花蜜，翅膀因振动而模糊。背景是一片郁郁葱葱、色彩缤纷的花园，带有柔和的焦外虚化效果，营造出梦幻般的氛围。这张图像细节极其丰富，以浅景深拍摄，确保焦点如刀锋般锐利地对准草莓蜂鸟，而背景则柔和地渐隐。高分辨率、专业摄影师风格和柔和的光线以非常细致的方式照亮整个场景，专业的调色放大了鲜艳的色彩，营造出异常清晰的画面。景深效果让蜂鸟与花朵在虚化的背景中格外突出。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/watermarked_photo_hummingbird_str.width-100.format-webp.webp)

Imagen 3 丰富细节与图像质量构图的示例

*注：本文底部可找到所有图像的提示词：陶艺师*
[8](#footnote-8)
*、松鼠*
[9](#footnote-9)
*、火车站*
[10](#footnote-10)
*、女子*
[11](#footnote-11)
*、草莓鸟*
[12](#footnote-12)

## Whisk：一个让你用图像作提示词、将想法可视化的有趣新工具

[Whisk](https://labs.google/fx/tools/whisk) 是我们来自 Google Labs 的最新实验，它让你输入或创建能够传达你心目中主体、场景和风格的图像。然后，你可以将它们组合起来、混搭再创作，生成独一无二的作品——从数字毛绒玩偶到珐琅徽章或贴纸，皆有可能。

在幕后，Whisk 将我们最新的 Imagen 3 模型与 Gemini 的视觉理解和描述能力相结合。Gemini 模型会自动为你的图像撰写详细的描述文字，然后将这些描述输入 Imagen 3。这一过程让你能够以有趣的新方式轻松混搭你的主体、场景和风格。

Whisk 今天在美国上线。[进一步了解 Whisk](https://blog.google/technology/google-labs/whisk)，并前往 [labs.google/Whisk](https://labs.google/fx/tools/whisk) 试用。
