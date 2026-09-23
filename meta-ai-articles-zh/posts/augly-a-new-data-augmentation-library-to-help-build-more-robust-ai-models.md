---
title: "AugLy：帮助构建更鲁棒 AI 模型的新数据增强库"
title_en: "AugLy: A new data augmentation library to help build more robust AI models"
date: 2021-06-17
source: http://ai.facebook.com/blog/augly-a-new-data-augmentation-library-to-help-build-more-robust-ai-models
crawled: 2026-09-22
translated: 2026-09-22
---

# AugLy：帮助构建更鲁棒 AI 模型的新数据增强库

> 原文：[AugLy: A new data augmentation library to help build more robust AI models](http://ai.facebook.com/blog/augly-a-new-data-augmentation-library-to-help-build-more-robust-ai-models) · Meta AI（Wayback 存档）

2021 年 6 月 17 日

**研究内容：**我们正在开源 AugLy——一个新的 Python 库，帮助 AI 研究者使用数据增强（data augmentation）来评估并改进机器学习模型的鲁棒性。增强可以包括对一段内容的各种修改，从重新裁剪照片到改变录音的音高。构建不被这些变化愚弄的 AI 十分重要。AugLy 通过提供复杂的数据增强工具来创建训练和测试不同系统的样本。AugLy 是一个新颖的开源数据增强库，结合音频、图像、视频和文本多种模态——这在许多 AI 研究领域正变得越来越重要。它提供 100 多种数据增强，聚焦于互联网上的真实用户在 Facebook 和 Instagram 等平台上对图像和视频所做的操作，例如叠加文本、表情符号以及截图变换。

使用真实世界的增强来组合不同模态——比如文本与图像、音频与视频——可以帮助机器更好地理解复杂内容。例如，「love the way you smell today」（喜欢你今天的气味）这句话的含义，在叠加到一张臭鼬图片上后会完全改变。这也更接近人们通过多种感官获取信息来了解世界的方式。随着数据集和模型愈发多模态，能够在统一的库和 API 下转换一个项目的全部数据非常有用。我们在 AugLy 中提供的数据增强集合，直接取材于我们在 Facebook 平台上观察到的数据变换类型，因此对从事社交媒体相关模型或数据工作的人尤其有用。

**工作原理：**AugLy 由我们西雅图和巴黎办公室的全球研究与工程师共同开发。它有四个子库，分别对应一种模态。每个库都遵循相同的接口：我们以函数式和类式两种格式提供变换，并提供强度函数帮助你理解一个变换有多「强烈」（基于给定参数）。AugLy 还能生成有用的元数据，帮助你理解数据是如何被变换的。我们聚合了许多来自不同现有库的增强，也包括一些我们自己编写的、此前从未有过的增强。例如，我们的一种增强会把图像或视频叠加到社交媒体界面上，使其看起来像是被用户在 Facebook 等社交网络上截图后再转发的。这对我们的用例（以及许多其他用例）是很有用的增强，因为 Facebook 上的人常以这种方式转发内容，而我们希望系统能够识别出：尽管有干扰性的界面元素，内容本身仍是同一份。

**为什么重要：**数据增强对确保 AI 模型的鲁棒性至关重要。如果我们能教会模型对数据中不重要属性的扰动保持鲁棒，模型就会学会聚焦于特定用例中数据的重要属性。在 Facebook，一个重要应用是检测特定内容的完全副本或近似副本。例如，同一条错误信息可能以略有不同的形式反复出现：裁剪掉几个像素的图像、加了滤镜或叠加了新文本的图像。用 AugLy 数据增强 AI 模型后，它们可以学会识别有人在上传已知侵权的内容（如歌曲或视频）。用 AugLy 训练近似副本检测模型，意味着我们或许能主动阻止用户上传已知侵权的内容。例如，SimSearchNet——我们专门为检测近似完全副本而构建的基于卷积神经网络的模型——就是用 AugLy 增强训练的。

除了用 AugLy 训练模型，该库还可以用来判定模型对一组增强的鲁棒性。事实上，AugLy 曾用于评估深度伪造检测挑战赛（Deepfake Detection Challenge）中深度伪造检测模型的鲁棒性，并最终影响了前五名获奖者的归属。AugLy 中的许多增强，源自我们观察到的人们为规避自动系统而变换内容的方式。例如，该库支持裁剪、填充图像、叠加梗图风格文字、截图并转发照片等图像增强。

数据增强的用途非常广泛。AugLy 可以帮助从事从物体检测模型、仇恨言论识别到语音识别的研究者。AugLy 是 Facebook AI 推进多模态机器学习更广泛努力的一部分——从 Hateful Memes 挑战赛到用于训练下一代购物助手的 SIMMC 数据集。

在此获取代码

**作者**

- Zoe Papakipos，研究工程师
- Joanna Bitton，软件工程师
