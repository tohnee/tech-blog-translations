---
title: "通过习得的等离子体控制加速聚变科学"
title_en: "Accelerating fusion science through learned plasma control"
source: https://deepmind.google/blog/accelerating-fusion-science-through-learned-plasma-control/
site: deepmind
date: 2022-02-16
crawled: 2026-09-13
translated: 2026-09-13
---

# 通过习得的等离子体控制加速聚变科学

> 原文：[Accelerating fusion science through learned plasma control](https://deepmind.google/blog/accelerating-fusion-science-through-learned-plasma-control/) · Google DeepMind

用深度强化学习成功控制托卡马克中的核聚变等离子体

注：本博客最初发表于 2022 年 2 月 16 日。随着 [TORAX 等离子体模拟器代码](https://github.com/google-deepmind/torax)于 2024 年 5 月发布，我们对文中内容做了小幅更新以反映这一点。

为了解决全球能源危机，研究人员长期以来一直在寻找一种清洁、无限的能源。核聚变——为宇宙中恒星提供能量的反应——是候选方案之一。通过撞击并聚合并氢（海水中的一种常见元素），这一强大的过程会释放巨大的能量。在地球上，科学家重建这些极端条件的一种方法是使用托卡马克（tokamak）——一种被磁线圈环绕的甜甜圈形真空容器，用来容纳温度比太阳核心还高的氢等离子体。然而，这些机器中的等离子体天然不稳定，使维持核聚变所需的过程成为一个复杂的挑战。例如，控制系统需要协调托卡马克的众多磁线圈，并以每秒数千次的频率调整其电压，以确保等离子体永不接触容器壁——一旦接触就会造成热量损失，甚至可能造成损坏。为帮助解决这一问题，并作为 DeepMind 推进科学使命的一部分，我们与 [EPFL（洛桑联邦理工学院）](https://www.epfl.ch/)的[瑞士等离子体中心](https://www.epfl.ch/research/domains/swiss-plasma-center/)合作，开发了首个深度强化学习（RL）系统，自主发现如何控制这些线圈，并成功在托卡马克中约束等离子体，为推进核聚变研究开辟了新途径。

在今天发表于 Nature 的[论文](https://www.nature.com/articles/s41586-021-04301-9)中，我们描述了如何通过在瑞士洛桑的变截面托卡马克（TCV）上构建并运行控制器，成功控制核聚变等离子体。使用一种结合深度 RL 与模拟环境的学习架构，我们造出的控制器既能保持等离子体稳定，又能将其精确地塑造成不同形状。这种"等离子体塑形"表明 RL 系统成功控制了过热物质——而且重要的是——它让科学家能够研究等离子体在不同条件下的反应，从而加深我们对聚变反应堆的理解。

> 过去两年里，DeepMind 已经展示了 AI 加速科学进步、开辟全新研究途径的潜力，涵盖生物学、化学、数学，如今又到了物理学。

Demis Hassabis（德米斯·哈萨比斯）

DeepMind 联合创始人兼 CEO

这项工作是机器学习与专家社区携手攻克重大挑战、加速科学发现的又一个有力例证。我们的团队正努力将这一方法应用于量子化学、纯数学、材料设计、天气预报等不同领域，以解决根本性问题，确保 AI 造福人类。

![变截面托卡马克（TCV）硬件的复杂工业级全景，展示密集的金属管道、支撑结构、电线与科学设备网络。](https://lh3.googleusercontent.com/WMw93KCG9rWNf9A7SsocGn4JFtXmm4XoVEtYgarEkv0rxR4HLLLXegV6o3fAWWML2zYAav4iS-CZEyEZOi0s6jXxhL0w9dtvEAaJqXFdE83ZJ5kG6s8=w1440)

![甜甜圈形托卡马克反应堆的简化 3D 剖面图，展示其灰色外部真空容器、缠绕其上的同心磁线圈，以及悬浮在内部的橙黄色核聚变等离子体核心。](https://lh3.googleusercontent.com/yY5FdXBZ4IMfow7lM9FxNH3DGAQ4cgb_w7T-lA9kCElgN6QDH4uQkQo_7VsmDgLXnIZTcr6MrKrgEtn7w7cAx2YKtjD2ebwG-j7HMcdZszwM0k41nEM=w1440)

![洛桑变截面托卡马克（TCV）空置真空容器的内部广角视图，展示其覆有保护瓦片的弧形金属壁和中央立柱。](https://lh3.googleusercontent.com/i3UG0ZGwTpjIW3jK5kIQVIpOcZ_56AUi-kac74MrxZ5u0MHcXbW61sOcFUnNWBjpSXQvR7mSBI0JHIZLZvcRh80ufVtG4jLsmzvMHLlY8k7AeAV4=w1440)

## 在数据难以获取时学习

核聚变研究目前受限于研究者开展实验的能力。虽然全球有数十台在运行的托卡马克，但它们造价高昂且需求旺盛。例如，TCV 在单次实验中最多只能维持等离子体三秒，之后需要 15 分钟冷却复位才能进行下一次尝试。不仅如此，多个研究组常常共用一台托卡马克，进一步压缩了可用的实验时间。

鉴于当前获取托卡马克的种种障碍，研究人员转向模拟器来推进研究。例如，我们在 EPFL 的合作伙伴构建了一套强大的模拟工具，用于对托卡马克的动力学建模。我们得以利用这些工具让 RL 系统先在模拟中学会控制 TCV，然后在真实的 TCV 上验证结果，证明我们可以成功将等离子体塑造成目标形状。虽然这是训练控制器更便宜、更方便的方式，我们仍需克服许多障碍。例如，等离子体模拟器速度很慢，模拟一秒的真实时间需要多个小时的计算机时。此外，TCV 的状态会日复一日地变化，这要求我们开发物理与模拟两方面的算法改进，并适应硬件的实际状况。

## 以简洁与灵活为先取得成功

现有的等离子体控制系统非常复杂，需要为 TCV 的 19 个磁线圈分别配备独立的控制器。每个控制器都用算法实时估计等离子体的属性，并相应调整磁体的电压。相比之下，我们的架构只用单个神经网络同时控制所有线圈，直接从传感器自动学习什么样的电压组合能实现目标等离子体位形。

作为演示，我们首先展示了只用一个控制器就能操纵等离子体的许多方面。

![动画分屏对比，左侧为托卡马克内部实时发光的蓝色等离子体实验画面，右侧为对应的数字等离子体状态重构图，随时间改变形状与位置。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622156ac3fb17333dc4ed11e_Fig202.gif)

用深度强化学习训练的控制器引导等离子体经历实验的多个阶段。左边是实验期间托卡马克的内部视角。右边可以看到重构的等离子体形状以及我们希望命中的目标点。（图片来源：DeepMind & SPC/EPFL）

在上面的视频中，我们看到我们的系统接管控制的瞬间，等离子体位于 TCV 的顶部。我们的控制器首先按请求的形状对等离子体塑形，然后将等离子体向下移动并使其脱离器壁，以两条"腿"将其悬浮在容器中部。等离子体保持静止，就像测量等离子体属性时需要的那样。最后，等离子体被引回容器顶部并被安全地熄灭。

随后，我们创建了一系列等离子体物理学家正在研究的形状，这些形状因其在产能方面的价值而受到关注。例如，我们制造了一种带有多条"腿"的"雪花"位形，它可以把排出能量分散到容器壁的不同接触点，帮助降低冷却成本。我们还演示了一种接近在建下一代托卡马克 [ITER](https://www.iter.org/) 方案的位形——当时 EPFL 正在开展实验以预测 ITER 中等离子体的行为。我们甚至完成了 TCV 上从未有人做过的事情：稳定一个"液滴"位形，让容器内同时存在两个等离子体。我们的单一系统能够为所有这些不同条件找到控制器。我们只需更改请求的目标，算法就会自主找到合适的控制器。

![托卡马克截面的五张示意图，展示由强化学习成功控制的不同等离子体形状：液滴（Droplets）、负三角形（Negative Triangularity）、类 ITER 形状（ITER-like shape）、雪花（Snowflake）和拉长等离子体（Elongated Plasma）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622156e74a5e0732d8c7268e_Fig203.gif)

我们成功产生了一系列等离子体物理学家正在研究其属性的形状。（图片来源：DeepMind & SPC/EPFL）

## 聚变的未来及更广阔前景

与我们将 AI 应用于其他科学领域时看到的进展类似，这次托卡马克控制的成功演示展现了 AI 加速并辅助聚变科学的力量，我们预计未来对 AI 的使用会日趋成熟。这种自主创建控制器的能力可以用来设计新型托卡马克，并同时设计它们的控制器。我们的工作也预示着强化学习在复杂机器控制领域的光明前景。尤其令人兴奋的是那些 AI 可以增强人类专业知识的领域——作为一种工具，为艰难的现实问题发现新颖而富有创造性的方案。我们预测，在未来数年，强化学习将成为工业与科学控制应用的变革性技术，应用范围从能源效率到个性化医疗。

2024 年 5 月，我们发布了 [TORAX](https://arxiv.org/abs/2406.06718)，一个新的[开源](https://github.com/google-deepmind/torax)等离子体模拟器。TORAX 对等离子体的"核心"（内部）建模，预测温度、密度和电流的变化。这拓展了我们训练先进托卡马克 AI 控制器的能力。TORAX 用 JAX 编写——JAX 是一个最初为训练 AI 而开发的 Python 框架——通过快速且可扩展的计算、更高的预测精度和敏感性分析，为科学计算提供了激动人心的能力。我们希望将 TORAX 及这些新能力开放给聚变社区，能够推动面向通用托卡马克设计与优化的新工作流程的开发。

**注记**

阅读论文：[Magnetic control of tokamak plasmas through deep reinforcement learning](https://www.nature.com/articles/s41586-021-04301-9)（通过深度强化学习实现托卡马克等离子体的磁控制）

阅读论文：[TORAX: A Fast and Differentiable Tokamak Transport Simulator in JAX](https://arxiv.org/abs/2406.06718)（TORAX：基于 JAX 的快速可微托卡马克输运模拟器）
