---
title: "教 AI 用更像人类的方式看世界"
title_en: "Teaching AI to see the world more like we do"
source: https://deepmind.google/blog/teaching-ai-to-see-the-world-more-like-we-do/
site: deepmind
date: 2025-11-11
crawled: 2026-09-13
translated: 2026-09-13
---

# 教 AI 用更像人类的方式看世界

> 原文：[Teaching AI to see the world more like we do](https://deepmind.google/blog/teaching-ai-to-see-the-world-more-like-we-do/) · Google DeepMind

**听文章** 10 分钟

新研究表明，重新组织模型的视觉表征，可以让它更有用、更稳健、更可靠

「视觉」人工智能（AI）无处不在。我们用它整理照片、识别不知名的花、驾驶汽车。但这些强大的系统并不总是像我们一样「看」世界，它们有时会表现出令人惊讶的行为。例如，一个能识别数百个汽车品牌和车型的 AI 系统，可能仍然无法捕捉汽车与飞机之间的共性——*即*两者都是以金属为主的大型载具。

为了更好地理解这些差异，今天我们在 [Nature 上发表了一篇新论文](https://www.nature.com/articles/s41586-025-09631-6)，分析了 AI 系统组织视觉世界的诸多重要方式与人类有何不同。我们提出了一种方法，可以更好地让这些系统与人类知识对齐，并证明解决这些差异能够提升它们的稳健性和泛化能力。

这项工作是朝着构建更直观、更可信赖的 AI 系统迈出的一步。

## 为什么 AI 会「找不同」失败

当你看到一只猫时，你的大脑会构建一个心理表征，捕捉关于这只猫的一切，从颜色、毛茸茸程度等基础概念，到「猫性」这样的高层概念。AI 视觉模型同样会产生表征：它把图像映射到高维空间中的点，相似的物品（比如两只羊）被放在相近的位置，不同的物品（一只羊和一块蛋糕）则相距甚远。

为了理解人类表征与模型表征在组织方式上的差异，我们采用了认知科学中经典的「找不同」（odd-one-out）任务，让人类和模型从三张给定图片中挑出哪一张与其余两张不属同类。这项测试能揭示它们「看到」的哪两个物品最相似。

有时，大家的看法一致。给一只貘、一只羊和一块生日蛋糕，人类和模型都能可靠地挑出蛋糕。但另一些时候，正确答案并不明确，人与模型就会产生分歧。

有意思的是，我们还发现很多情况下人类对答案有强烈共识，而 AI 模型却做错了。以下面第三个例子为例，大多数人都认为海星是那个「不同」的，但大多数视觉模型更关注背景颜色、纹理等表面特征，于是选了猫。

![三行「找不同」图像三元组，对比人类与 AI 的分类。第一行是貘、羊和一块生日蛋糕，标注为「对齐」（Aligned），因为人类和 AI 都选了蛋糕。第二行是柠檬、红色电话亭和一只瞪羚，标注为「不明确」（Unclear），因为人类判断各不相同。第三行是狐狸、海星和猫，标注为「不对齐」（Unaligned），因为人类选出海星作为「不同」项，而 AI 错误地选了猫。](https://lh3.googleusercontent.com/qYpkuEX0oANy3iSQVsowLqlNrgEOxhbtcTwe23fKWQyqURoZruzejU_gUvbZDInicRi7VbvbjX5yh3pXclLyEOD38QCAgrH2qm1jMKND16EteM-J6dM=w1440)

「找不同」任务的三个例子。三行分别展示自然界中三个主体的一组图片。第一行是一个人类与模型一致认同的简单任务。第二行是人类与 AI 模型存在分歧的例子。第三行是人类倾向于一致、而模型做出不同选择的例子。

这个例子说明了人类与 AI 之间存在系统性的错位，我们在从图像分类器到无监督模型的许多不同视觉模型中都观察到了这一现象。

这个整体问题可以在 AI 内部映射图的一个二维投影（PCA）中看到。

下面左图是一个视觉模型的内部映射图，它看起来毫无结构，动物、食物、家具等不同类别的表征混杂在一起。右边的结构是我们应用对齐方法后改进的表征映射图，类别得到了清晰的组织。

![两张散点图，对比不对齐分类器与对齐分类器的内部表征映射图。左侧「不对齐分类器」（Unaligned classifier）图呈现出高度混杂、杂乱无章的彩色数据点，代表不同类别的点相互纠缠，水牛、蜘蛛和草的图像彼此紧挨。右侧「对齐分类器」（Aligned classifier）图则显示出清晰分离、彼此区隔的彩色簇，对应食物（绿色）、动物（蓝色）、家具（红色）等类别，同样的三张图像彼此相距很远，反映出它们在概念上的差异。](https://lh3.googleusercontent.com/JeGjvW3BHrbEoNFaag8o4EEgOqesvS5NKVuqjc5cVpz6FTSRKbUFpPR2AiW5wjZcRFRCKcbO8JWCTWUO-S031cGWcBJ7HuygrsHDJ7kSthZuFH92zw=w1440)

两张映射图展示了一个视觉模型对许多不同类别物品的表征。对齐之前（左）看不到任何组织结构。对齐之后（右）表征按类别得到了有意义的组织。

## 多步对齐方法

认知科学家已经收集了包含数百万条人类「找不同」判断的 [THINGS](https://things-initiative.org/) 数据集，我们本可以用它来帮助解决视觉对齐问题。遗憾的是，这个数据集只使用了几千张图片——信息量不足以直接微调强大的视觉模型，模型会立刻在这一小部分图片上过拟合，并遗忘许多既有技能。

为了解决这个问题，我们提出了一个三步方法：

1. 我们从一个强大的预训练视觉模型（SigLIP-SO400M）出发，基于 THINGS 数据集在其上精心训练一个小型适配器。通过冻结主模型并对适配器训练进行仔细的正则化，我们得到了一个不会遗忘先前训练的教师模型（teacher model）。
2. 随后，这个教师模型充当类人判断的替身，我们用它生成了一个名为 [AligNet](https://github.com/google-deepmind/alignet?tab=readme-ov-file#alignet-dataset) 的大规模新数据集，基于一百万张不同的图片得到了数百万条类人「找不同」决策——远超我们可能从真人那里收集到的数量。
3. 最后，我们用这个新数据集微调其他 AI 模型（即「学生模型」，student model）。由于我们数据集的多样性，过拟合不再是问题，学生模型可以得到充分训练，并更深入地重构其内部映射。

如下方示意图所示，学生模型的表征从杂乱无章变成了结构清晰的组织形式，动物（蓝色）、食物（绿色）等高层概念与其他类型的物体彼此分离。

![一个三步流程示意图，说明对齐方法：1）使用线性适配器在 THINGS 数据集上训练教师模型；2）利用教师模型从 ImageNet 生成大规模三元组相似度数据集（AligNet）；3）将这些自举（bootstrapped）相似度蒸馏进学生模型。](https://lh3.googleusercontent.com/vrR1IgBevAiwEmZOT5I-myaPoKaW7sSwTmkPRpaovn0h64lLfn7SchZJ4sGyxIn7DRplbGf7wqFcVXr_9hDKmfV9z0zWhC025qHbFoJVjP9aOORMpw=w1440)

我们三步模型对齐方法的示意图。

人类知识按照不同的相似度层级组织。当我们把模型与人类知识对齐时，模型的表征也会按照这些相似度层级发生变化。这种重组遵循认知科学已揭示的人类知识的层级结构。

在对齐过程中，我们可以看到表征按照其在人类类别层级中的「概念距离」成比例地相互靠近或远离。例如，两只狗（同一从属类别）会相互靠近（距离减小），而猫头鹰与卡车（不同的上级类别）则会相互远离（距离增大）。

![左侧是一张折线图，纵轴为密度，横轴为相对距离变化，绘制了四个类别层级。右侧示意图以层级结构展示这些类别：「不同上级类别」（黄色，比较卡车与猫头鹰）、「同一上级类别」（红色，比较猫头鹰与贵宾犬）、「同一基础类别」（紫色，比较贵宾犬与金毛寻回犬）、「同一从属类别」（黑色，比较两只金毛寻回犬）。图上相应颜色的曲线表明，在对齐过程中，相近类别的物品（黑色和紫色）距离减小（曲线左移），而不同上级类别的物品（黄色）距离增大（曲线右移）。](https://lh3.googleusercontent.com/Pc9gCB67xt6YI0xKqWuxsaKotVNfI_QfvUXxSVW17sFFcUDYJWV0-rzFAuhcPemINu3G3KKUkvNVLJaUlPUoQpCoX7sw6r0AEvFYmuK59PRym2Tq=w1440)

一张折线图展示人类表征与 AI 表征之间相对距离的变化。非常相似类别的表征倾向于相互靠近，而相似度较低的物品对的表征则倾向于相互远离。

我们可以得出结论：我们的方法按照人类概念层级组织了 AI 学生模型的表征映射，而且无需对此进行显式监督。

## 测试对齐后的模型

我们在许多认知科学任务上测试了对齐后的模型——包括多排列（multi-arrangement）等任务，即按照相似度对许多图片进行排列——以及我们自行收集的一个名为 [Levels](https://doi.gin.g-node.org/10.12751/g-node.hg4tdz/) 的新「找不同」数据集。在每一种情况下，对齐后的模型都展现出了显著提升的人类对齐度，在一系列视觉任务中与人类判断的吻合频率大幅提高。

我们的模型甚至学到了一种「类人」的不确定性。在测试中，模型决策的不确定性与人类做选择所花的时间——不确定性的常用替代度量——高度相关。

我们还发现，让模型更符合人类认知，也能让它们整体上成为更好的视觉模型。对齐后的模型在各类具有挑战性的任务上表现好得多，例如从单张图片学习一个新类别（「小样本学习」），或者在被测图片类型发生变化（「分布偏移」）时仍能做出可靠决策。

![标题为「人类对齐度」（Human alignment）的柱状图，对比原始模型（浅灰）与 AligNet 对齐模型（蓝色）在认知科学任务上的准确率。在「三元组找不同」（Triplet odd-one-out）任务上，AligNet 在两组实验中的准确率都显著高于原始模型；在「多排列」（Multi-arrangement）任务上，AligNet 的准确率大幅超越原始模型。](https://lh3.googleusercontent.com/EuxuEhBLzvT2srQ3HQvltTxwBwZ0BiwQlW9cUEJu1ReDabAz3PdkjVTSI09J102zjQBsg6kjS8PG0Tp-551477JzVpzjgNEaZ5onJWTaPH9UktgN_nE=w1440-h810-n-nu)

![标题为「泛化」（Generalisation）的柱状图，对比原始模型（浅灰）与 AligNet 对齐模型（蓝色）在 AI 任务上的表现。在小样本学习（Few-shot learning）与分布偏移（Distribution shift）两类任务中，AligNet 模型始终显著优于原始模型。](https://lh3.googleusercontent.com/UvkD3RRITqF906Y5QqwVHxResI3wu5YNKGsprbeVfMxg6lTHOmwZU8Bh10eJpjAUQBpZ3mVWWKR9-dsGDdcYwaqPK8YoxqtNTVmC7i-HrqizK2Mp=w1440-h810-n-nu)

两张柱状图表明，在对齐模型（深蓝）在涉及找不同与多排列的认知科学任务（上）以及涉及小样本学习与分布偏移的 AI 任务（下）上都优于原始模型（浅灰）。

## 迈向更符合人类认知、更可靠的模型

许多现有的视觉模型无法捕捉人类知识的更高层结构。这项研究提出了一种可能的解决方法，并表明模型可以更好地与人类判断对齐，同时在各种标准 AI 任务上表现得更可靠。

虽然对齐工作仍有许多要做，但我们的工作展示了朝着更稳健、更可靠的 AI 系统迈出的一步。

进一步了解我们的工作

[阅读我们的论文](https://www.nature.com/articles/s41586-025-09631-6)[基于开源实现进行开发](https://github.com/google-deepmind/alignet)[在 Levels 数据集上评测模型](https://doi.gin.g-node.org/10.12751/g-node.hg4tdz/)

## 致谢

我们感谢论文第一作者 Lukas Muttenthaler，以及我们的合作者 Frieda Born、Bernhard Spitzer、Simon Kornblith、Michael C. Mozer、Klaus-Robert Müller 和 Thomas Unterthiner。
