---
title: "Grok-1.5 Vision 预览版"
title_en: "Grok-1.5 Vision Preview"
date: 2025-03-12
source: https://x.ai/news/grok-1.5v
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok-1.5 Vision 预览版

> 原文：[Grok-1.5 Vision Preview](https://x.ai/news/grok-1.5v) · xAI

2024 年 4 月 12 日

用我们的第一个多模态模型连接数字世界与物理世界。

---

**介绍 Grok-1.5V，我们的第一代多模态模型。除了强大的文本能力之外，Grok 现在可以处理多种视觉信息，包括文档、图表、示意图、截图和照片。Grok-1.5V 很快将向我们的早期测试者和现有 Grok 用户开放。**

## 能力

Grok-1.5V 在多个领域与现有前沿多模态模型具有竞争力，涵盖多学科推理以及理解文档、科学示意图、图表、截图和照片。我们尤其对 Grok 理解物理世界的能力感到兴奋。在我们衡量真实世界空间理解的新基准 RealWorldQA 上，Grok 优于同类模型。对于下表中的所有数据集，我们在零样本、无思维链提示的设置下评测 Grok。

| 基准 | **Grok-1.5V** | GPT-4V | Claude 3 Sonnet | Claude 3 Opus | Gemini Pro 1.5 |
| --- | --- | --- | --- | --- | --- |
| MMMU 多学科 | 53.6% | 56.8% | 53.1% | **59.4%** | 58.5% |
| Mathvista 数学 | **52.8%** | 49.9% | 47.9% | 50.5% | 52.1% |
| AI2D 示意图 | 88.3% | 78.2% | **88.7%** | 88.1% | 80.3% |
| TextVQA 文字识别 | **78.1%** | 78.0% | - | - | 73.5% |
| ChartQA 图表 | 76.1% | 78.5% | 81.1% | 80.8% | **81.3%** |
| DocVQA 文档 | 85.6% | 88.4% | **89.5%** | 89.3% | 86.5% |
| RealWorldQA 真实世界理解 | **68.7%** | 61.4% | 51.9% | 49.8% | 67.5% |

示例

从示意图写出代码

![一张描述猜数字游戏的示意图，包含游戏逻辑和用户交互的流程图](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgrok1.5v_guessing.4bae7361.webp&w=2048&q=75)

##### 用户

你能把它翻译成 Python 代码吗？

##### Grok

当然可以！你提供的流程图描述了一个简单的猜数字游戏：计算机生成一个随机数，用户需要猜出它。下面是与流程图逻辑对应的 Python 代码：

python

```
import random

def guess_number(): # Generate a random number between 1 and 10

    target = random.randint(1, 10)

    while True:
        guess = int(input("Guess a number between 1 and 10: "))

        if guess == target:
            print("You won!")
            break
        else:
            print("Wrong guess, try again!")

if __name__ == "__main__":
    guess_number()
```

这段代码将按流程图所述运行猜数字游戏。用户会被提示输入猜测，直到猜中正确的数字为止。

## 真实世界理解

要开发实用的真实世界 AI 助手，提升模型对物理世界的理解至关重要。为此，我们推出一个新基准 RealWorldQA。该基准旨在评测多模态模型的基础真实世界空间理解能力。当前基准中的许多示例对人类来说相对容易，但常常给前沿模型带来挑战。

![桌上摆放着各种家居用品的照片。](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frealworldqa_sample_1.40f61ece.webp&w=3840&q=75)

哪个物体更大，披萨刀还是剪刀？A. 披萨刀更大。B. 剪刀更大。**C. 它们大小差不多。**

![一条昏暗街道的照片，路牌上写着 "left lane must turn left"](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frealworldqa_sample_2.c56d23d9.webp&w=3840&q=75)

从当前车道可以往哪里走？**A. 左转。** B. 直行。C. 左转并直行。D. 右转。

![一条街道的照片，左侧停着几辆车](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frealworldqa_sample_3.8c909fbe.webp&w=3840&q=75)

根据我们轿车前摄像头的画面，我们是否有足够的空间绕过前面的灰色汽车？**A. 有。** B. 没有。

![一个玩具旁边放着一部显示指南针的手机的照片。](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frealworldqa_sample_4.510a61d4.webp&w=1920&q=75)

根据图片，恐龙面朝哪个基本方向？A. 北。B. 南。**C. 东。** D. 西。

RealWorldQA 的首发版本包含 700 多张图像，每张图像配有一个问题和易于验证的答案。数据集由车辆拍摄的匿名化图像以及其他真实世界图像组成。我们很高兴向社区发布 RealWorldQA，并打算随着多模态模型的进步不断扩充它。RealWorldQA 以 [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/?ref=chooser-v1) 许可发布。点击[这里（677MB）](https://data.x.ai/realworldqa.zip)下载数据集。

## 走向未来

推进我们的多模态理解与生成能力，是构建能够理解宇宙的有益 AGI 的重要一步。未来几个月，我们预期将在图像、音频、视频等多种模态上对这两方面能力做出重大改进。

如果你想参与这段旅程，我们正在[招聘](/careers)。

在以下平台试用 Grok

[网页](https://grok.com)

[iOS](https://apps.apple.com/app/grok/id6670324846)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[Grok on X](https://x.com/i/grok)

产品

[Grok](/grok)

[API](/api)

公司

[公司简介](/company)

[招聘](/careers)

[联系我们](/contact)

[新闻](/news)

资源

[状态](https://status.x.ai)

[隐私政策](/privacy-policy)

[安全](/security)

[法律](/legal)
