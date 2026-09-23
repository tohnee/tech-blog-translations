---
title: "结合 Transformer 与卷积神经网络，构建更好的计算机视觉模型"
title_en: "Better computer vision models by combining Transformers and convolutional neural networks"
date: 2021-07-08
source: https://ai.facebook.com/blog/computer-vision-combining-transformers-and-convolutional-neural-networks
crawled: 2026-09-22
translated: 2026-09-22
---

# 结合 Transformer 与卷积神经网络，构建更好的计算机视觉模型

> 原文：[Better computer vision models by combining Transformers and convolutional neural networks](https://ai.facebook.com/blog/computer-vision-combining-transformers-and-convolutional-neural-networks) · Meta AI（Wayback 存档）

**这项研究是什么：**我们开发了一种名为 ConViT 的新计算机视觉模型，它结合了两种广泛使用的 AI 架构——卷积神经网络（CNN）与基于 Transformer 的模型——以克服每种方法单独使用时的一些重要局限。通过同时借助这两种技术，这个基于视觉 Transformer 的模型能够超越现有架构，尤其是在小数据场景下，同时在大数据设定下达到相近的性能。

AI 研究者在构建新机器学习模型和训练范式时，常常采用一组特定假设——通常称为归纳偏置（inductive bias）——因为这有助于模型从更少的数据中学到更泛化的解。CNN 已在视觉任务上极为成功，它依赖内置于架构本身的两条归纳偏置：彼此邻近的像素是相关的（局部性），以及图像的不同部分应被同等处理而与其绝对位置无关（权重共享）。相比之下，基于自注意力的视觉模型（如 Data-efficient image Transformers 和 Detection Transformers）的归纳偏置极少。在大数据集上训练时，这类模型已经追平有时甚至超越 CNN 的表现；但在小数据集上训练时，它们往往难以学到有意义的表示。

因此 AI 研究者面临一个权衡：CNN 的强归纳偏置使其即使数据极少也能达到高性能（高下限），但这些归纳偏置也可能在数据充足时限制模型（低上限）。相反，Transformer 的归纳偏置极少，这在少数据设定中可能成为限制（低下限），但这种灵活性又使 Transformer 在大数据场景下超越 CNN（高上限）。

我们将在本月 ICML 2021 上展示的工作提出了一个简单的问题：能否设计这样的模型——当归纳偏置有帮助时受益于它，而当数据中可以学到更好的解时又不被它限制？换句话说，我们能否两全其美？为此，我们的 ConViT 模型用「软」卷积归纳偏置做初始化，必要时模型可以学会忽略它。软归纳偏置可以帮助模型学习而不构成束缚。硬归纳偏置（如 CNN 的架构约束）可以大幅提升学习的样本效率，但当数据集规模不是问题时可能变得掣肘。ConViT 引入的软归纳偏置通过在不需要时自行消退，避免了这一限制。

**工作原理：**我们对视觉 Transformer 加以改造，施加一种软卷积归纳偏置——它鼓励网络以卷积方式运作，但关键在于允许模型自行决定是否保持卷积。为施加这一软归纳偏置，我们引入了门控位置自注意力（gated positional self-attention，GPSA）——一种位置自注意力形式，模型在其中学习一个门控参数 lambda，控制标准基于内容的自注意力与卷积初始化的位置自注意力之间的平衡。

（ConViT（左）是 ViT 的一个变体，其中部分自注意力（SA）层被替换为门控位置自注意力层（GPSA；右）。由于 GPSA 层涉及位置信息，类别 token 在最后一个 GPSA 层之后才与隐藏表示拼接。FFN：前馈网络（两个线性层，中间夹 GeLU 激活）；W qry：查询权重；W key：键权重；v pos：注意力中心与跨度嵌入（可学习）；r qk：相对位置编码（固定）；λ：门控参数（可学习）；σ：sigmoid 函数。）

配备 GPSA 层后，ConViT 超越了近期提出的同等规模与计算量的 Data-efficient image Transformers（DeiT）模型。例如，ConViT-S+ 略优于 DeiT-B（82.2% 对 81.8%），而参数量仅为其一半多一点（48M 对 86M）。不过，ConViT 的改进在数据受限的场景中最为显著——此时软卷积归纳偏置发挥更大作用。例如，当只使用 5% 的训练数据时，ConViT 大幅超越 DeiT（47.8% 对 34.8%）。

（ConViT 在样本效率和参数效率上都优于 DeiT。左：我们通过在 ImageNet-1k 的子集上以相同超参数训练 ConViT-S 与 DeiT-S 来比较样本效率，绿色显示 ConViT 相对 DeiT 的改进幅度。右：我们比较 ConViT 模型与其他视觉 Transformer（菱形）和 CNN（方形）在 ImageNet-1k 上的 top-1 准确率。其他模型在 ImageNet 上的表现取自 Touvron et al., 2020；He et al., 2016；Tan & Le, 2019；Wu et al., 2020；以及 Yuan et al., 2021。）

除了性能优势，门控参数还为我们提供了一种简便方式，来理解每层在训练后保留卷积特性的程度。在所有层中，我们发现随着训练推进，ConViT 对卷积位置注意力的关注逐渐减少。对较后面的层，门控参数最终收敛到接近 0，表明卷积归纳偏置实际上被忽略了；而对较早的层，许多注意力头保持较高的门控值，表明网络在早期层利用卷积归纳偏置辅助训练。

（该图展示了 DeiT（b）与 ConViT（c）的若干注意力图示例。σ(λ) 表示可学习的门控参数：接近 1 的值表示正在使用卷积初始化，接近 0 的值表示只使用基于内容的注意力。注意 ConViT 的早期层部分保留了卷积初始化，而后期层则纯粹基于内容。）

**为什么重要：**AI 模型的性能极大地依赖于训练数据的类型与数量。在研究中——在现实世界应用中更是如此——我们常常受限于可用的数据。我们相信，ConViT——以及更广泛地，施加模型可学会忽略的软归纳偏置这一思想——是朝着构建更灵活、无论拿到什么数据都能表现良好的 AI 系统迈出的重要一步。ConViT 还通过提供可解释的参数帮助我们更好地理解这些模型的工作方式，可用来理解和调试它们。（Facebook AI 也在以其他方式探索可解释性，例如模型可解释性开源库 Captum、关于易于解释神经元的功能作用的研究，以及关于「彩票」初始化的研究。）

我们希望 ConViT 方法能激励社区探索其他从硬归纳偏置走向软归纳偏置的途径。为此，我们已在 GitHub 上提供代码，模型也已集成进流行的 Timm 与 VISSL 库。

阅读完整论文

**作者**

- Ari Morcos，研究科学家
- Stephane d'Ascoli，研究助理
- Levent Sagun，研究科学家
