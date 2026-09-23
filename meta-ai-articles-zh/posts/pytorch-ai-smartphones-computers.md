---
title: "PyTorch 如何把 AI 的力量带到电脑和智能手机上"
title_en: "How PyTorch is bringing the power of AI to computers and smartphones"
date: 2022-12-02
source: https://ai.facebook.com/blog/pytorch-ai-smartphones-computers
crawled: 2026-09-22
translated: 2026-09-22
---

# PyTorch 如何把 AI 的力量带到电脑和智能手机上

> 原文：[How PyTorch is bringing the power of AI to computers and smartphones](https://ai.facebook.com/blog/pytorch-ai-smartphones-computers) · Meta AI（Wayback 存档）

2022 年 12 月 2 日

人们在 Facebook 和 Instagram 上喜爱的许多体验都由人工智能（AI）驱动。其中不少功能——如 Assistant、Avatars（虚拟化身）和 AR 特效——由于延迟、网络带宽等限制，无法依靠服务器端 AI 实现。在设备端运行 AI——即直接在手机、平板电脑甚至一副智能眼镜上运行——相比不断把数据回传服务器有巨大优势：它更快，也为使用我们平台的用户带来了增强隐私的体验。不过，设备端 AI 也带来了新挑战，因为必须应对电池容量小、处理器远不如数据中心服务器强大、内存更少的设备。今天，我们将进一步分享 Meta 如何利用 PyTorch——这一我们与 AI 共同体一同开发、如今已是 Linux 基金会一部分的开源机器学习框架——把更多 AI 驱动的体验带到个人设备上。

为了提供最佳的 AI 产品体验，AI 模型需要根据其部署设备的不同约束条件进行优化。各团队反复迭代 AI 模型，以在电池续航、功耗、算力、体积和内存占用方面达到最先进水平。这正是 PyTorch 能派上用场的地方。PyTorch 打造了让开发者能在种类繁多的设备上高效、高性能执行 AI 模型的基础设施。PyTorch 移动运行时足够小巧，可以适配众多移动设备，同时支持编写这些 AI 模型所用的各种算子，并可在不同计算资源上进行优化。

2021 年，我们宣布将所有 AI 系统迁移到 PyTorch。如今 PyTorch 驱动着 Meta 全线产品使用的机器学习（ML）技术栈和工作流工具，借助自 1.9 版本起就在开源版本中提供的同一套方案（PyTorch Mobile）来扩大设备端 AI 的应用规模。我们看到这些设备端生产用例呈指数级增长。

在 Meta 的移动应用家族中，PyTorch 设备端运行承担着：

- 每日 700 亿次推理
- 跨不同移动应用的 50 个设备端 AI 模型
- Instagram、Facebook、Messenger 和 Meta Spark 的全部设备端机器学习

我们的设备端 AI 还支撑着 Meta 移动应用中的若干关键用例。以下是几个例子：

- 实时视频通话：我们的视频背景选择模型让人们在视频通话时可以选择虚化或独特的 AR 背景，从而在自己的空间里获得更私密的交流体验。
- 保护隐私的机器学习：在 Messenger 等产品中，我们的模型在设备端对用户的动态（Feed）和好友列表进行排序，以更私密的方式完成预测，所需数据保留在用户自己的设备上。
- 商业诚信：我们的文本和图像模型检测并封杀「隐身伪装」信息流广告（cloaking feed ads），这是恶意行为者试图在我们的平台上触达用户的一种手段。
- 智能定向快速推广（Smart Target Quick Promotion）：快速推广（Quick Promotion）是一个让 Facebook 通过动态（Feed）、通知和 Messenger 等产品及时、精准地与用户沟通的平台，涵盖产品信息和公共公告。借助 PyTorch，我们为快速推广上线了基于设备端 AI 的更智能定向算法。

PyTorch 还为 Instagram Reels 上更引人入胜的 AI 体验提供支持，人们可以通过可以「试戴」的 AR 特效来创建内容，比如更换背景、为自拍添加有趣的 AR 特效和体验。

在最近发布的 Meta Quest Pro 上，Reality Labs 利用 PyTorch 实现了手部与眼部追踪、自然面部表情（Natural Facial Expressions）和键盘追踪等能力。

## PyTorch 驱动的设备端体验的未来

我们相信 AI 正在推动新产品和新体验的创造，并能进一步提升现有产品的能力。随着 PyTorch 把 AI 直接带到设备上运行，这只会为进一步创新打开大门，带来更高的可靠性、交互性和隐私性。基于我们在种类繁多的设备上支持应用和用户的经验，我们相信可以把设备端 AI 的技术前沿继续向前推进。

明年，我们将推出面向设备端 AI 的下一代 PyTorch 框架，它将在更多设备（包括微控制器）上实现效率、性能和可移植性的阶跃式提升，同时与 PyTorch 其余部分保持一致，便于部署。

## 作者

Raziel Alvarez Guevara

软件工程师

Christian Keller

产品经理

Chakri Uddaraju

工程经理
