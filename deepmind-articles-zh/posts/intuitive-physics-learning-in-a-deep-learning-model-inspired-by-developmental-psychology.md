---
title: "受发展心理学启发的深度学习模型中的直觉物理学习"
title_en: "Intuitive physics learning in a deep-learning model inspired by developmental psychology"
source: https://deepmind.google/blog/intuitive-physics-learning-in-a-deep-learning-model-inspired-by-developmental-psychology/
site: deepmind
date: 2022-07-11
crawled: 2026-09-13
translated: 2026-09-13
---

# 受发展心理学启发的深度学习模型中的直觉物理学习

> 原文：[Intuitive physics learning in a deep-learning model inspired by developmental psychology](https://deepmind.google/blog/intuitive-physics-learning-in-a-deep-learning-model-inspired-by-developmental-psychology/) · Google DeepMind

理解物理世界是大多数人都能毫不费力运用的一项关键技能。然而，这对人工智能来说仍然是一个挑战；如果我们要在现实世界中部署安全且有益的系统，我们希望这些模型能与我们共享对物理学的直觉。但在构建这些模型之前，还有另一个挑战：我们如何衡量这些模型理解物理世界的能力？也就是说，"理解物理世界"意味着什么，我们又该如何量化它？

所幸的是，发展心理学家们已经花费数十年时间研究婴儿对物理世界的认知。在此过程中，他们把"物理知识"这一模糊概念细化为一组具体的物理概念。而且，他们还开发了期望违背（violation-of-expectation，VoE）范式，用于在婴儿身上测试这些概念。

在我们今天发表于《自然·人类行为》（Nature Human Behavior）的论文中，我们扩展了他们的工作，并开源了 [Physical Concepts 数据集](https://github.com/deepmind/physical_concepts)。这个合成视频数据集将 VoE 范式移植过来，用于评估五种物理概念：坚固性（solidity）、客体永存性（object persistence）、连续性（continuity）、"不可变性"（unchangeableness）和方向性惯性（directional inertia）。

有了衡量物理知识的基准之后，我们转向构建一个能够学习物理世界的模型。这一次，我们再次从发展心理学家那里寻找灵感。研究人员不仅记录了婴儿对物理世界知道什么，还提出了能够支撑这种行为的机制。尽管各有差异，这些理论解释都有一个共同的核心：将物理世界分解为一组随时间演化的物体。

受这项工作的启发，我们构建了一个昵称为 PLATO（Physics Learning through Auto-encoding and Tracking Objects，通过自编码与物体追踪学习物理）的系统。PLATO 把世界表示为一组物体并据此进行推理。它根据物体过去的位置以及它们与其他物体的交互情况，预测它们未来将出现在哪里。

在简单物理交互的视频上训练 PLATO 之后，我们发现 PLATO 通过了 Physical Concepts 数据集中的所有测试。此外，我们还训练了与 PLATO 一样大（甚至更大）、但不使用基于物体的表示的"扁平"模型。当我们测试这些模型时，发现它们未能通过全部测试。这表明物体表示有助于学习直觉物理，为发展心理学文献中的相关假说提供了支持。

我们还想知道发展这种能力需要多少经验。早在两个半月大的婴儿身上就已观察到具备物理知识的证据。相比之下，PLATO 的表现如何？通过改变 PLATO 所使用的训练数据量，我们发现 PLATO 只需 28 小时的视觉经验就能学会这些物理概念。由于我们的数据集规模有限且是合成的，我们无法在婴儿与 PLATO 所接受的视觉经验量之间做严格的同类比较。不过，这一结果表明：如果借助"把世界表示为物体"这一归纳偏置（inductive bias）的支持，直觉物理可以通过相对较少的经验习得。

最后，我们想测试 PLATO 的泛化能力。在 Physical Concepts 数据集中，测试集中的所有物体也都出现在训练集中。如果我们用 PLATO 从未见过的物体来测试它会怎样？为此，我们利用了 MIT 研究人员开发的另一个合成[数据集](http://physadept.csail.mit.edu/)的一个子集。这个数据集同样用于探测物理知识，只是视觉外观不同，且包含 PLATO 从未见过的一组物体。PLATO 在没有任何重新训练的情况下通过了测试，尽管测试所用的是全新的刺激。

我们希望这个数据集能帮助研究人员更具体地理解其模型理解物理世界的能力。未来，可以通过增加所测物理概念的数量，并使用更丰富的视觉刺激——包括新的物体形状，甚至真实世界的视频——来扩展对直觉物理更多方面的测试。
