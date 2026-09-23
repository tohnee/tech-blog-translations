---
title: "Alta Daily 如何利用 Meta 的 Segment Anything 重新构想数字衣橱"
title_en: "How Alta Daily Uses Meta's Segment Anything to Reimagine the Digital Closet"
date: 2026-04-06
source: https://ai.meta.com/blog/alta-daily-fashion-app-segment-anything
crawled: 2026-09-22
translated: 2026-09-22
---

# Alta Daily 如何利用 Meta 的 Segment Anything 重新构想数字衣橱

> 原文：[How Alta Daily Uses Meta's Segment Anything to Reimagine the Digital Closet](https://ai.meta.com/blog/alta-daily-fashion-app-segment-anything) · Meta AI（Wayback 存档）

2026 年 4 月 6 日 · 阅读约 5 分钟

据估计，大多数人只穿衣柜里 20% 的衣服，但其余的并非无用，而是尚未开发的潜力：有些搭配之所以从未成型，是因为记住自己拥有什么——更别提想象它们如何组合在一起——比听起来难得多。AI 时尚应用 Alta Daily 正是基于这一洞察打造的。Alta Daily 应用于 2025 年上线，用户可以拍下自己的全部衣物并数字化。借助自然语言提示，应用从用户的数字衣橱中为任何场合推荐完美穿搭，并展示穿在用户个人 Alta 虚拟形象上的效果。它还能记录用户每天的穿着，让避免重复穿搭变得容易。

Alta 工程负责人 Joon Kim 的虚拟形象上一个月的穿搭，由 SAM 3 分割。

Alta 的核心是 Meta 的 Segment Anything Model（SAM），它已被用于分割和数字化数百万套服装。从一开始，Alta Daily 的创始人兼 CEO Jenny Wang 就知道自己想打造一款具有「干净美感」的应用，把人们拥有的衣物像时尚杂志页面上那样陈列。这意味着要去除每一张用户上传图片的背景——这项任务被证明是重大的技术障碍。

「我们调研了各种分割模型，」Wang 说，「时尚尤其是最复杂的图像数据集之一，特别因为用户上传内容的不一致性。比如白墙前的一只白色运动鞋，或者室内糟糕光线下摊在皱巴巴蓝色毯子上的蓝色毛衣——那很难分割。」

团队还必须应对其他具有挑战性的场景：合适的模型需要捕捉珠宝的精细细节，确保反光表面不会改变真实颜色；还需要能围绕细衣架和真人模特进行分割。Alta 团队在从太阳镜到鞋类的八个商品类别上测试了各种分割模型，发现 Meta 的 Segment Anything Model 始终能交付最佳效果。SAM 能处理从镜前自拍到铺在地毯上的物品等各种图像，是其成功的关键因素。

图中展示了 SAM 1 与 SAM 3 之间的改进。

「如果我们知道上传的每张图都是漂亮的模特大片，分割会容易得多，但由于用户上传内容的特性，我们需要最好的分割能力。」Wang 说，「SAM 3 让我们能够打造干净的杂志编辑风界面，让数字穿搭成为一种无缝而愉悦的体验。」

除了性能出众，SAM 还给公司带来了显著的经济影响。Wang 还记得自己最初考察的外部分割 API 的价格令她「震惊」——每张图要花几美分。「这累积起来非常快，尤其当你想到用户每秒上传多少张图时。」她说，「作为早期公司，你追求最好的体验，但也对成本保持清醒。你得打造人们喜爱的产品，同时知道自己没有无限的资金。」通过使用 SAM，Alta 团队已处理超过 2000 万张图片而没有产生高昂成本，得以专注于为用户打造最好的产品。该应用已经收获全球拥趸，在美国、法国、德国、墨西哥和荷兰拥有坚实的用户群。

未来，Alta 团队希望新的 AI 研究能帮助他们创造更沉浸的体验。团队已经在试验 Meta 的 SAM 3D 模型，这可能解锁用户与数字 Alta 虚拟形象互动的新方式。「我们什么都玩，」Wang 说，「我们喜欢试验新模型。我们有一个庞大的时尚专用数据集，并且不断在模型之间跑评测。」

在 AI 和 SAM 这类开源模型的帮助下，Alta 正帮助人们表达个人风格、充分发挥衣橱的潜力。正如 Wang 所说：「有了 AI，我们终于可以构建下一代购物与穿搭体验。」

下载 Alta Daily

阅读更多关于 SAM 3 的内容
