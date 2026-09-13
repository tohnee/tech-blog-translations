---
title: "用 AI 更深入地感知宇宙"
title_en: "Using AI to perceive the universe in greater depth"
source: https://deepmind.google/blog/using-ai-to-perceive-the-universe-in-greater-depth/
site: deepmind
date: 2025-09-04
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 AI 更深入地感知宇宙

> 原文：[Using AI to perceive the universe in greater depth](https://deepmind.google/blog/using-ai-to-perceive-the-universe-in-greater-depth/) · Google DeepMind

我们新颖的 Deep Loop Shaping 方法改进了引力波天文台的控制，帮助天文学家更好地理解宇宙的动力学与形成过程。

为了帮助天文学家研究宇宙中最剧烈的过程，我们的团队一直在利用 AI 来稳定有史以来最灵敏的观测仪器之一。

在今天发表于 Science 的论文中，我们介绍了 [Deep Loop Shaping](https://www.science.org/doi/10.1126/science.adw1291)——一种新颖的 AI 方法，将开启下一代引力波科学。Deep Loop Shaping 降低了天文台反馈系统中的噪声并改进其控制，帮助稳定用于测量引力波的部件——引力波是时空结构中的微小涟漪。

这些波由中子星碰撞、黑洞并合等事件产生。我们的方法将帮助天文学家收集理解宇宙动力学与形成所必需的关键数据，并更好地检验物理学与宇宙学的基础理论。

我们与加州理工学院运营的 [LIGO](https://www.ligo.caltech.edu/)（激光干涉引力波天文台）以及 [GSSI](https://www.gssi.it/)（格兰萨索科学研究所）合作开发了 Deep Loop Shaping，并在路易斯安那州利文斯顿的天文台上验证了我们的方法。

LIGO 以惊人的精度测量引力波的性质与来源。但最轻微的振动也会干扰它的测量——哪怕振动来自 100 英里外拍打墨西哥湾海岸的海浪。为了正常运转，LIGO 依靠数千个控制系统让每个部件保持近乎完美的对齐，并通过连续反馈适应环境扰动。

Deep Loop Shaping 将 LIGO 中最不稳定、最困难的反馈回路的噪声水平降低了 30 到 100 倍，提升了其高灵敏干涉仪镜面的稳定性。将我们的方法应用于 LIGO 的所有镜面控制回路，可以帮助天文学家每年多探测并收集数百个事件的数据，细节也远比现在丰富。

未来，Deep Loop Shaping 还可以应用于许多其他涉及振动抑制、噪声消除以及高动态或不稳定系统的工程问题，这些在航空航天、机器人技术和结构工程中都很重要。

## 测量整个宇宙

LIGO 利用激光的干涉来测量引力波的性质。通过研究这些性质，科学家可以推断出引力波由什么产生、来自何处。天文台的激光在相距 4 公里的镜面之间反射，这些镜面安置在世界上最大的真空腔中。

![LIGO 利文斯顿天文台的航拍照片，显示一座中央设施，两条相互垂直的长真空腔臂伸入茂密的绿色森林。](https://lh3.googleusercontent.com/oa12R2qqeKIQawk5Ua9FF1be-tOiMmGe3i-EMZfqY4lf-P7KcVcPOdZMC_cMR-teUVv2NzXJwCVFiSqR7KPooYgQ4mv6_P2xArGQ_STZWFX_dyYIEQ=w1440)

美国路易斯安那州利文斯顿的 LIGO（激光干涉引力波天文台）航拍图。天文台的激光在相距 4 公里的镜面之间反射。图片由 Caltech/MIT/LIGO Lab 提供。

自 2015 年首次探测到由一对碰撞黑洞产生的引力波、[验证了阿尔伯特·爱因斯坦广义相对论的预言](https://www.ligo.caltech.edu/news/ligo20160211)以来，LIGO 的测量深刻改变了我们对宇宙的理解。

借助这座天文台，天文学家已探测到数百次黑洞与中子星碰撞，证实了双黑洞系统的存在，目睹了在中子星碰撞中形成的新黑洞，研究了金等重元素的产生，等等。

天文学家对最大和最小的黑洞已有很多了解，但关于中等质量黑洞的数据仍然有限——它被认为是理解星系演化的「缺失环节」。

到目前为止，LIGO 只能观测到极少数这类系统。为了帮助天文学家捕捉这一现象更多的细节和数据，我们致力于改进控制系统中最困难的部分，并扩展我们能观测到这些事件的距离。

> 用引力而不是光来研究宇宙，就像是在聆听而不是观看。这项工作让我们能够调到低音频道。

Rana Adhikari

加州理工学院物理学教授，2025 年

## 降低噪声、稳定系统

当引力波穿过 LIGO 的两条 4 公里长的臂时，会使它们之间的空间发生形变，改变两端镜面之间的距离。这些微小的长度差异用光干涉来测量，精度达到 10^-19 米——相当于质子尺寸的万分之一。面对如此微小的测量，LIGO 的探测器镜面必须保持极度静止，与环境扰动隔绝。

![一个高度复杂的多级机械悬挂系统，在 LIGO 天文台的真空腔内悬挂着一片大型反射式圆形干涉仪镜面。](https://lh3.googleusercontent.com/DGB5pVjZE7PO6faNiwHKyQQtPtO3Ln8JViSmr0ZjdDhvu8iQieL6Hx7--HG8O-gQ8VHQdX9Xskq4BY7aBfgH30WNT-rNvxKdIcfw_K4VRfetcZLo=w1440)

LIGO 的特写照片。LIGO 使用强激光与镜面探测宇宙中的引力波，这些波由黑洞碰撞与并合等事件产生。图片由 Caltech/MIT/LIGO Lab 提供。

这需要一套系统做被动机械隔离，另有一套控制系统做主动振动抑制。控制太少，镜面会晃动，什么都测不了；控制太多，反而会放大系统中的振动而不是抑制它们，在某些频率范围内把信号淹没。

这些振动被称为「控制噪声」，是提升 LIGO 探测宇宙能力的关键障碍。我们的团队设计 Deep Loop Shaping，旨在超越传统方法——例如目前使用的线性控制设计方法——把控制器本身从一个显著的噪声来源中移除。

## 更有效的控制系统

Deep Loop Shaping 采用一种使用频域奖励的强化学习方法，超越了最先进的反馈控制性能。

在一个模拟的 LIGO 环境中，我们训练了一个控制器，它尽量避免放大用于测量引力波的观测频带内的噪声——在这个频带里，我们需要镜面保持静止，才能观测到高达数百个太阳质量的黑洞并合等事件。

![](https://lh3.googleusercontent.com/0Uvd3fF1PS3xNgVJSXruw84j1Fiu8734Gm49ZvujSAzoqhy3HlsF9UPLgtbLNry46s8uA1wHKi1C06XZAhkMz2gCLiUbHMVrySrxNqWPvxZNOJ2a6A=w1440-h810-n-nu)

通过在频域奖励引导下的反复交互，控制器学会了抑制观测频带内的控制噪声。换言之，我们的控制器学会在不引入有害控制噪声的情况下稳定镜面，把噪声水平降低到十倍或更多，低于反射自镜面的光辐射压中[由量子涨落引起](https://www.caltech.edu/about/news/ligo-surpasses-the-quantum-limit)的振动量。

## 在模拟与硬件上都表现强劲

我们在美国路易斯安那州利文斯顿的真实 LIGO 系统上测试了我们的控制器——发现它们在硬件上的表现与在模拟中一样好。

我们的结果显示，Deep Loop Shaping 对噪声的控制效果比现有控制器好 30 到 100 倍，并首次把 LIGO 上最不稳定、最困难的反馈回路从显著的噪声来源中消除。

![一张折线图，对比现有线性控制器（红线）与新的 Deep Loop Shaping 神经网络控制策略（蓝线）在不同频率下的噪声水平。蓝线在大多数频率下明显低于红线，展示了控制噪声的大幅降低，并接近或超过了设计规格量子极限（绿色虚线）。](https://lh3.googleusercontent.com/Ipt51zpd_jDIqEgOKyNGNkIBkBtnOP6-Ay9Y8Xj89sNA8oApb7GSgAilmoODPqARSscDI8JT6WAfBYs5nQ-o7gPXonMe7A4VTLp0CkmO5PbyZmXoKw=w1440)

折线图展示使用我们 Deep Loop Shaping 方法得到的控制噪声频谱。在最不稳定、最困难的反馈控制回路中，注入控制噪声水平改善了 30 至 100 倍。

在重复实验中，我们确认了控制器能让天文台系统长时间保持稳定。

## 更好地理解宇宙的本质

Deep Loop Shaping 通过解决研究引力波的关键障碍，拓展了天体物理学目前可能性的边界。

将 Deep Loop Shaping 应用于 LIGO 的整套镜面控制系统，有望消除来自控制系统自身的噪声，为其宇宙学观测能力的扩展铺平道路。

除了显著改进现有引力波天文台对更远、更暗弱源的测量之外，我们期待这项工作能影响未来天文台——无论是在地球上还是在太空中——的设计，并最终首次串联起遍布宇宙的缺失环节。

**进一步了解我们的工作**

[阅读我们的论文](https://www.science.org/stoken/author-tokens/ST-2883/full)[阅读 Caltech 博客](https://www.caltech.edu/about/news/artificial-intelligence-helps-boost-ligo)[阅读 GSSI 博客](https://gssi.it/communication/news-events/item/25900-ai-turns-up-the-volume-on-the-universe)[了解 LIGO](https://www.ligo.caltech.edu/page/learn-more)

**致谢**

本研究由 Jonas Buchli、Brendan Tracey、Tomislav Andric、Christopher Wipf、Yu Him Justin Chiu、Matthias Lochbrunner、Craig Donner、Rana X Adhikari、Jan Harms、Iain Barr、Roland Hafner、Andrea Huber、Abbas Abdolmaleki、Charlie Beattie、Joseph Betzwieser、Serkan Cabi、Jonas Degrave、Yuzhu Dong、Leslie Fritz、Anchal Gupta、Oliver Groth、Sandy Huang、Tamara Norman、Hannah Openshaw、Jameson Rollins、Greg Thornton、George van den Driessche、Markus Wulfmeier、Pushmeet Kohli、Martin Riedmiller 完成，是 LIGO、Caltech、GSSI 与 GDM 的合作成果。

我们感谢出色的 LIGO 仪器团队不知疲倦地保障天文台持续运行，并支持我们的实验。
