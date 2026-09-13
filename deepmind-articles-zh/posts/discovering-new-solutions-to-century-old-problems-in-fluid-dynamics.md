---
title: "为流体力学中的百年难题发现新解"
title_en: "Discovering new solutions to century-old problems in fluid dynamics"
source: https://deepmind.google/blog/discovering-new-solutions-to-century-old-problems-in-fluid-dynamics/
site: deepmind
date: 2025-09-18
crawled: 2026-09-13
translated: 2026-09-13
---

# 为流体力学中的百年难题发现新解

> 原文：[Discovering new solutions to century-old problems in fluid dynamics](https://deepmind.google/blog/discovering-new-solutions-to-century-old-problems-in-fluid-dynamics/) · Google DeepMind

我们的新方法可以帮助数学家借助 AI 技术攻克数学、物理和工程领域长期存在的挑战。

几个世纪以来，数学家们发展出复杂的方程来描述流体力学中的基础物理规律。这些定律支配着一切——从飓风的旋涡，到托起机翼的气流。

专家可以精心构造一些让理论与实践相悖的场景，得出在物理上永远不可能发生的情形。这些情形——例如速度或压强等量变为无穷大——被称为「奇点」（singularities）或「爆破」（blow ups）。它们帮助数学家识别流体力学方程的根本性局限，并加深我们对物理世界如何运转的理解。

在[一篇新论文](https://arxiv.org/abs/2509.14185)中，我们为一些描述流体运动的最复杂方程引入了一族全新的数学爆破解。这项工作是与来自布朗大学、纽约大学和斯坦福大学等机构的数学家和地球物理学家合作完成的。

我们的方法展示了一条利用 AI 技术攻克数学、物理和工程中长期挑战的新途径，这些挑战要求前所未有的精度与可解释性。

## 不稳定奇点的重要性

稳定性是奇点形成的关键属性。如果一个奇点对微小变化保持稳健，它就是稳定的；反之，不稳定奇点则需要极端精确的条件。

数学界普遍预期，不稳定奇点在流体力学的基础性问题中扮演重要角色，因为数学家相信，在复杂的无边界的 3D [欧拉方程](https://en.wikipedia.org/wiki/Euler_equations_(fluid_dynamics))和[纳维-斯托克斯方程](https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_equations)中不存在稳定奇点。在纳维-斯托克斯方程中找到任何奇点，是至今未解的六大著名[千禧年大奖难题](https://www.claymath.org/millennium-problems/)之一。

借助我们新颖的 AI 方法，我们首次系统地发现了横跨三种不同流体方程的多个不稳定奇点新家族。我们还观察到，随着解变得越来越不稳定，一个模式随之浮现：刻画爆破速度的参数 λ（lambda），可以相对于不稳定阶数——即解偏离爆破方式的独立途径数目——绘制出来。这一模式在所研究的两个方程中清晰可见：不可压多孔介质方程（IPM）和布辛涅斯克方程（Boussinesq）。这暗示还存在更多不稳定解，其假设的 λ 值落在同一条线上。

![一张折线图，纵轴为「λ 的倒数」，横轴为 0 到 4 的「不稳定阶数」，显示两条向上倾斜的线性关系：一条实线蓝线代表「带边界的 IPM」，一条虚线紫线代表「Boussinesq」。](https://lh3.googleusercontent.com/VoRTLG1YRAcdn0K32JuI5Pp0VK--Rzk8MZILQkr3zrkWLMSbOscSFmJohznpHnlI6mQ4V450Ud7ZDmrrwrst7NfRRfR_mjGEmJa9f3vncd371xeFWjE=w1440)

折线图展示我们的结果：随着我们找到越来越不稳定的解，代表爆破速度的关键参数 λ 在两个方程——不可压多孔介质方程（IPM）与布辛涅斯克方程——中都呈现出惊人清晰的模式。

我们通过引入二阶优化器等用于训练神经网络的机器学习技术发现了这些奇点。这些方法使我们把精度提升到了前所未有的水平。作为参照，我们所消除的最大误差，相当于把地球直径预测到几厘米的范围之内。

这里我们展示了为所研究方程之一找到的涡量（Ω）场示例。涡量度量流体在每一点的旋转程度。

![涡量（Ω）场的三维图，绘制在 y₁ 与 y₂ 轴上，呈现一个光滑的弯曲曲面，从其峰值处的蓝色过渡到最低点的紫色。](https://lh3.googleusercontent.com/DwpT60RGTClvrbwFAZvO6umLh0LuVKLzKubY139lJOsFFpOqfFFsBCYCwmB50jVaBoiHwmlRjgD0AFFt_LkRyrjGQqVoqqPF3bF2wVpE36Vz21Lc=w1440)

为所研究方程之一找到的三维表征及其二维涡量（Ω）场的可视化。

我们还针对发现的所有不稳定情形，沿一个坐标轴展示了同一场的一维切片，呈现日益不稳定的奇点的演化过程。

![一张折线图，纵轴为涡量（$\\Omega$），横轴为空间坐标 $y^1$，五条曲线代表不同不稳定程度：「稳定」「一阶不稳定」「二阶不稳定」「三阶不稳定」「四阶不稳定」。随着不稳定性增加，曲线从光滑低幅的波（稳定）逐渐变为在 $y^1 = -1$ 与 $y^1 = 1$ 附近越来越尖锐、幅度越来越大的峰与谷。](https://lh3.googleusercontent.com/VF1U6W9G6b2lhxjLLEXv-XKHdSfAXctoufRyMiFGWKi84X9rNMyjK5I20DfRiAuqOpbBfa3PdPOfzfxdfBpemfUBJ3RaNA9KCpa7gv3mo-5gxDDDWQ=w1440)

为所研究方程之一找到的三维表征及其二维涡量（Ω）场的可视化。

## 新颖方法在浩瀚的奇点图景中穿行

我们的方法基于物理信息神经网络（Physics-Informed Neural Networks，PINNs）。与从海量数据中学习的常规神经网络不同，我们训练模型去匹配描述物理定律的方程。网络的输出会被不断对照物理方程的预期进行检验，并通过最小化其「残差」——即其解未能满足方程的程度——来学习。

> 通过嵌入数学洞见并达到极限精度，我们把 PINNs 转变成了一个能找到 elusive 奇点（难以捉摸的奇点）的发现工具。

Yongji Wang

该研究第一作者、纽约大学博士后研究员

我们对 PINNs 的使用超越了它们作为求解偏微分方程（[PDE](https://en.wikipedia.org/wiki/Partial_differential_equation)）通用工具的典型角色。通过把数学洞见直接嵌入训练过程，我们得以捕捉那些长期挑战传统方法的难以捉摸的解——例如不稳定奇点。

与此同时，我们开发了一个高精度框架，把 PINNs 推向接近机器精度，从而达到了严格计算机辅助证明所需的精确度水平。

## 计算机辅助数学的新时代

这一突破代表了一种新的数学研究方式：把深刻的数学洞见与前沿 AI 相结合。我们期待这项工作能帮助开启一个新时代——用 AI 和计算机辅助证明攻克长期悬而未决的难题。

**了解更多**

[阅读我们的论文](https://arxiv.org/abs/2509.14185)

**致谢**

本工作由以下人员共同完成：Yongji Wang、Mehdi Bennani、James Martens、Sébastien Racanière、Sam Blackwell、Alex Matthews、Stanislav Nikolov、Gonzalo Cao-Labora、Daniel S. Park、Martin Arjovsky、Daniel Worrall、Chongli Qin、Ferran Alet、Borislav Kozlovskii、Nenad Tomašev、Alex Davies 和 Pushmeet Kohli

以及 Tristan Buckmaster、Bogdan Georgiev、Javier Gómez-Serrano、Ray Jiang 和 Ching-Yao Lai。
