---
title: "用 SynthID 识别 AI 生成的图像"
title_en: "Identifying AI-generated images with SynthID"
source: https://deepmind.google/blog/identifying-ai-generated-images-with-synthid/
site: deepmind
date: 2023-08-29
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 SynthID 识别 AI 生成的图像

> 原文：[Identifying AI-generated images with SynthID](https://deepmind.google/blog/identifying-ai-generated-images-with-synthid/) · Google DeepMind

新工具帮助为 Imagen 创建的合成图像添加水印并进行识别

AI 生成的图像每天都在变得更流行。但我们要如何更好地识别它们，尤其是在它们看起来如此逼真的情况下？

今天，我们与 [Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-next-2023-announcements) 合作，推出 [SynthID](https://deepmind.google/blog/in-conversation-with-ai-building-better-language-models/) 的测试版——一个用于为 AI 生成图像添加水印并进行识别的工具。这项技术将数字水印直接嵌入图像的像素之中，人眼无法察觉，但可以检测出来用于识别。

SynthID 将向有限数量的 [Vertex AI](https://cloud.google.com/vertex-ai) 客户发布，供其配合 [Imagen](https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview) 使用——后者是我们最新的文生图模型之一，能够根据输入文本创建逼真的照片级图像。

![](https://lh3.googleusercontent.com/WeBR_JIbLo0Sd1tKfJkPTW9EzO44KJHqsVfPtH09b3W1qWRyEjrV7iLXkqRCjTE8z0X_jC8vOL2KB-ux2AjWe2aLfBmEb8lYaX6BQSkFLDsaimrFUdo=w1440-h810-n-nu)

生成式 AI 技术正在迅速演进，计算机生成的图像（也称为「合成图像」）越来越难以与并非由 AI 系统创作的图像区分开来。

虽然生成式 AI 能够释放巨大的创造潜力，但它也带来了新的风险，例如让创作者可以有意或无意地传播虚假信息。能够识别 AI 生成的内容至关重要，它能让人们在接触生成式媒体时心中有数，并有助于防止错误信息的传播。

我们致力于让人们获取高质量的信息，并维护整个社会中创作者与用户之间的信任。这份责任的一部分，就是为用户提供更先进的 AI 生成图像识别工具，使其图像——乃至某些经过编辑的版本——能够在日后被识别出来。

![一段 GIF，旋转展示四张不同的 AI 生成图像。每张图像沿中垂线一分为二，左侧为加水印的版本，右侧为不加水印的版本。两者之间没有明显差异。四张图像分别是：一只插画风熊走过小木屋、一头照片级写实奶牛站在草坡上、身后有山，一只犰狳的黑白特写照片，以及一只正在湖边饮水的插画风火烈鸟。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/64e8abbb424b8a7e3b88b707_64e7629196215db21326c003_synthid_watermark_lo.gif)

SynthID 为 AI 生成图像生成难以察觉的数字水印。

Google Cloud 是第一家提供负责任地创建 AI 生成图像、并可靠识别这些图像的工具的云服务商。这项技术植根于我们开发与部署负责任 AI 的理念，由 Google DeepMind 研发，并与 Google Research 合作完善。

SynthID 并不能抵御极端的图像篡改，但它为赋能个人和组织负责任地使用 AI 生成内容提供了一条有前景的技术路径。这一工具还可以伴随其他 AI 模型和图像之外的模态（如音频、视频和文本）一同演进。

## AI 图像的新型水印

水印是一种可以叠加在图像上以识别它的设计。从纸张上的物理印记，到今天数码照片上常见的半透明文字和符号，水印在历史长河中不断演进。

传统水印不足以识别 AI 生成的图像，因为它们通常像印章一样盖在图像上，很容易被编辑掉。例如，位于图像角落的离散水印可以用基本的编辑技术裁剪掉。

在「难以察觉」与「对图像篡改的鲁棒性」之间找到恰当的平衡非常困难。高度可见的水印——通常作为一层带有名称或标志的内容叠加在图像上方——对创意或商业用途来说也存在美观上的问题。同样，一些先前开发的不可见水印会在缩放尺寸等简单编辑操作中丢失。

![八宫格网格展示一张紫色蝴蝶图像的不同修改版本，演示了模糊、灰度、蓝色色调、旋转、色彩滤镜、噪声和亮度调整等多种变化。](https://lh3.googleusercontent.com/6J5kRoU6TtjW7_CWcaVJj_lwK9TsnnSB1K2_okt11aKPmQl9iCGituySYuGvvUVbqdt_3jy03r1L1s9FxKy98WW3o89vGQKU9YRbhTTZFgLxkuPp=w1440)

即使经过添加滤镜、更改颜色和亮度等修改，水印依然可以被检测到。

我们在设计 SynthID 时确保它不会损害图像质量，并让水印在经过添加滤镜、更改颜色、以及以各种有损压缩方案（最常用于 JPEG）保存等修改之后，依然保持可检测。

SynthID 使用两个深度学习模型——一个用于加水印，一个用于识别——它们是在多样化的图像集上共同训练的。组合模型在一系列目标上进行优化，包括正确识别带水印的内容，以及通过让水印与原始内容在视觉上对齐来提升不可察觉性。

## 鲁棒且可扩展的方法

SynthID 让 Vertex AI 客户能够负责任地创建 AI 生成图像，并可靠地识别它们。虽然这项技术并不完美，但我们的内部测试表明，它对许多常见的图像篡改都能保持准确。

SynthID 的组合式方法：

- **加水印**：SynthID 可以为 Imagen 生成的合成图像添加不可察觉的水印。
- **识别**：通过扫描图像中的数字水印，SynthID 可以评估一张图像由 Imagen 创建的可能性。

![一张文字表格，展示用于指示识别置信度的符号。绿色对勾标注「检测到数字水印」，表示该图像很可能由 Imagen 生成。灰色叉号标注「未检测到数字水印」，表示该图像不太可能由 Imagen 生成。黄色三角形内含感叹号，标注「可能检测到数字水印」，表示该图像可能是生成的，请谨慎对待。](https://lh3.googleusercontent.com/RcNmIRkeMo3OZBjK_X1Htx2KspARIV86qcwKkArLdXgZvnTiy0SQugW8loRb--PbGoMO-yhSxcOZlo-qRiYx2SSlVh4bXr2iG6LRpvLnGh37LfNouOk=w1440)

SynthID 可以帮助评估一张图像由 Imagen 创建的可能性。

这一工具提供三个置信度等级，用于解读水印识别的结果。如果检测到数字水印，则图像的一部分很可能由 Imagen 生成。

SynthID 是识别数字内容的众多方法之一。最常用的内容识别方法之一是元数据（metadata），它提供诸如创作者是谁、创建时间等信息。这些信息与图像文件存储在一起。添加到元数据中的数字签名随后可以显示图像是否被更改过。

当元数据信息完好时，用户可以轻松识别一张图像。然而，元数据可能被手动删除，甚至在文件编辑时丢失。由于 SynthID 的水印嵌入在图像的像素之中，它与基于元数据的其他图像识别方法兼容，并且在元数据丢失的情况下仍可被检测到。

## 下一步是什么？

为了负责任地构建 AI 生成内容，[我们承诺在每一个环节都开发安全、可靠、值得信赖的方法](https://www.whitehouse.gov/wp-content/uploads/2023/07/Ensuring-Safe-Secure-and-Trustworthy-AI.pdf)——从图像生成与识别，到媒介素养与信息安全。

随着生成式模型不断进步并扩展到其他媒介，这些方法需要保持鲁棒且可适应。我们希望 SynthID 技术能够与面向全社会创作者和用户的广泛解决方案协同工作。我们将继续通过收集用户反馈、增强其能力、探索新特性来演进 SynthID。

SynthID 有望扩展到其他 AI 模型上使用。我们期待在不久的将来把它集成到更多 Google 产品中，并向第三方开放——赋能个人和组织负责任地使用 AI 生成内容。

注：本博客中用于生成合成图像的模型可能与 Imagen 和 Vertex AI 上使用的模型有所不同。

[阅读 Google Cloud 公告](https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-next-2023-announcements)

**致谢**

本项目由 Sven Gowal 和 Pushmeet Kohli 领导，主要研究贡献来自（按字母顺序排列）：Rudy Bunel、Jamie Hayes、Sylvestre-Alvise Rebuffi、Florian Stimberg、David Stutz 和 Meghana Thotakuri。

感谢 Nidhi Vyas 和 Zahra Ahmed 推动产品交付；感谢 Chris Gamble 协助启动本项目；感谢 Ian Goodfellow、Chris Bregler 和 Oriol Vinyals 提供建议。其他贡献者包括 Paul Bernard、Miklos Horvath、Simon Rosen、Olivia Wiles 和 Jessica Yung。同时感谢 Google DeepMind 和 Google 各处众多做出贡献的同事，包括我们在 Google Research 和 Google Cloud 的合作伙伴。

![一只金属质感蝴蝶停在叶子上的 AI 生成图像](https://lh3.googleusercontent.com/ZS-zI46bM9R9lgYgMJfofqMF4KsacJmxHaAywxl3aKlzUOw4kbdMpaHwk4EiCPbchTLF05ShML4DEVFLT-9ev3dTBTK0EbyXncnpJOzQQ-FCZQ2LcA=w1440)

一只翅膀带有棱镜花纹的金属质感蝴蝶的加水印图像
