---
title: "表格数据的深度学习"
title_en: "Deep Learning for Tabular Data"
source: https://sebastianraschka.com/blog/2022/deep-learning-for-tabular-data.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 表格数据的深度学习

> 原文：[Deep Learning for Tabular Data](https://sebastianraschka.com/blog/2022/deep-learning-for-tabular-data.html)

[最后更新：2023 年 1 月 23 日]

在我的课程中，我强调深度学习真正擅长的是非结构化数据（本质上，这正是表格数据的反面）。深度学习有时被称为"表示学习"（representation learning），因为它的强项在于能够学习特征提取流程本身。而大多数表格数据集已经是（通常由人工）提取好的特征，因此在这些数据上使用深度学习不应有明显优势。

![Deep learning for tabular data unstructured structured](https://sebastianraschka.com/images/blog/2022/deep-learning-for-tabular-data/unstructured-structured.webp)

尽管如此，最近仍有许多研究者尝试为表格数据集开发专用的深度学习方法。我时不时会 在社交媒体上分享一些提出表格数据新深度学习方法的研究论文，这通常是很好的讨论引子。人们常常会要求补充更多方法或提出反例。所以在这篇短文中，我打算简要总结我目前所知的主要深度表格学习论文。我可能遗漏或忘掉了一些。我很乐意持续维护并更新这份清单以供日后参考，所以如果有我遗漏的内容，[请告诉我](https://twitter.com/rasbt/status/1551252319689400324)。

（顺带一提，许多更早的论文在表格数据集上使用多层感知机并称之为"深度学习"——我想起若干在分子指纹数据上训练多层感知机的计算生物学论文。不过在我看来，多层感知机算不上真正的"深度学习"，所以我不把它们列入。）

我想强调的是，无论深度表格方法看起来多么有趣或有前景，我仍然建议先用常规机器学习方法作为基线。我在[我的书](https://sebastianraschka.com/books/)中先讲常规机器学习、再讲深度学习，是有原因的。

## 表格数据深度学习论文（按时间倒序排列）

下面是一份（不断增长的）相关论文列表，附有链接和简短总结。随着新论文发表，我会尽量保持这份列表的更新。如果你知道一些我可能遗漏的论文，[请告诉我](https://twitter.com/rasbt/status/1551252319689400324)！

请注意，以下主题略微超出本文范围，因此不列入此列表：

- 经典深度学习方法（普通多层感知机等）；
- 为时间序列数据开发的方法；
- 与推荐系统相关的方法。

[最后更新：2022 年 11 月 21 日]

### 目录

---

[2022 年 10 月 12 日]

### 语言模型是逼真的表格数据生成器（2022-10）

作者：Vadim Borisov, Katrin Sessler, Tobias Leemann, Martin Pawelczyk, Gjergji Kasneci

📝 论文：<https://arxiv.org/abs/2210.06280>

🖥 代码：<https://github.com/kathrinse/be_great>

- GReaT（**G**eneration of **Rea**listic **T**abular data）方法使用基于[自注意力](https://sebastianraschka.com/glossary/#mha "Multi-Head Attention (MHA)")的自回归生成式 LLM 来生成合成的表格数据集；作者具体使用了预训练的 transformer 解码器网络（GPT-2 以及更小的 Distil-GPT-2）。
- GReaT 支持异构特征，包括离散特征和数值特征，并在四个数据集上进行了评估：Travel customers（25 万样本）、HELOC（1 万样本）、Adult Income（5 万样本）和 California Housing（2 万样本）。
- 作者利用预训练的 transformer，整个过程分为两个步骤：微调和采样。
- 第 1 阶段，微调：（1）把特征向量转换为文本；（2）打乱特征顺序以编码顺序无关性；（3）用文本对 transformer 进行微调。
- 第 2 阶段，采样：把（不完整的）输入传给微调后的 transformer；（2）从 transformer 获得以文本格式补全的特征向量；（3）把特征文本转换回表格格式。
- 在"机器学习效率"实验中，作者发现，与其他方法生成的合成数据相比，用 GReaT 合成数据训练的分类器表现更好（也更接近用原始数据训练的结果）。
- 在评估合成数据与原始数据的相似程度时，"最近记录距离"（distance to closest records）图显示 GReaT 并没有照搬训练数据。此外，作者还做了一项"判别器度量"研究：他们把原始数据与合成数据合并，并赋予类别标签以区分数据是原始的（0）还是合成的（1）。在这些数据集上训练的分类器平均准确率为 70%，说明它们在一定程度上能识别出人工数据。不过，GReaT 的表现远好于其他合成数据方法（这些方法的准确率在 75% 到 88% 之间）。

---

[2022 年 10 月 10 日]

### TabPFN：一种能在几秒内解决小型表格分类问题的 Transformer（2022-10）

作者：Noah Hollmann, Samuel Müller, Katharina Eggensperger, Frank Hutter

📝 论文：<https://arxiv.org/abs/2207.01848>

🖥 代码：<https://github.com/automl/TabPFN>

🐦 Twitter：[讨论帖](https://twitter.com/rasbt/status/1584210875455791104?s=20&t=Pnz4juqslqGFbID-lxLxzw)

- TabPFN（tabular prior-data fitted network）是对表格数据深度学习的一次引人入胜的全新尝试，它结合了近似贝叶斯推断和 transformer 分词。
- 注意，虽然该方法基于贝叶斯推断，但众所周知（参见 Judea Pearl 的 [Book of Why](https://en.wikipedia.org/wiki/The_Book_of_Why)），仅凭观测数据无法得到因果机制。作为一种巧妙的变通，研究者直接在给定一个可供采样的先验的情况下近似后验预测分布。
- 该方法特别吸引人的地方在于，它不需要训练、超参数调优或交叉验证——只需要在新训练集上做一次前向传播。代价是它需要用于先验的合成数据集。（在训练数据集上做常规超参数调优，难道不比昂贵的先验数据拟合过程更费劲吗？先验拟合需要 8 块 GPU 跑 20 小时。）
- 目前，该方法在 30 个小数据集（2 千训练样本、100 个特征、10 个不平衡类别）上进行了评估；在计算上，它无法很好地扩展到更大数据集，因为其计算量随训练集大小呈平方级增长。
- XGBoost、LightGBM、AutoGluon 等其他方法被限制在每个数据集 60 分钟的计算时间内。其他同时代的表格方法未纳入这次[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")。每个数据集上取得最佳成绩最多的是 TabPFN + AutoGluon 组合（9 次），其次是 AutoGluon（7 次）和 TabPFN（6 次）。XGBoost 只在 3 个数据集上胜过其他方法。
- 研究者提到，其误差与其他方法的误差不相关；这使得 TabPFN 很适合用于集成（ensembling），这可能是一个值得未来研究的有趣方向。

---

[2022 年 9 月 30 日]

### TabDDPM：用扩散模型对表格数据建模（2022-09）

作者：Akim Kotelnikov, Dmitry Baranchuk, Ivan Rubachev, Artem Babenko

📝 论文：<https://arxiv.org/abs/2209.15421>

🖥 代码：<https://github.com/rotot0/tab-ddpm>

🐦 Twitter：[解读与讨论帖](https://twitter.com/rasbt/status/1579110843081691136?s=20&t=SvEGtDykVUXhDUajtDrooA)

- TabDDPM 是一个用于生成合成表格数据的扩散模型，同时适用于类别特征和连续特征。
- TabDDPM 对类别（和二值）特征使用多项扩散，加入均匀噪声；对连续特征则使用常见的高斯扩散。逆向扩散过程通过一个全连接网络（多层感知机）学习。
- 研究者在 15 个分类和回归数据集上评估了 TabDDPM，训练样本数从 856 到 157,638 不等。
- 定性比较显示，与 TVAE、CTABGAN、CTABGAN+ 和 SMOTE 等其他技术相比，TabDDPM 生成的合成数据分布与训练数据分布最为接近。
- 在一项"机器学习效率"比较中，研究者在合成数据上训练了不同模型（随机森林、逻辑回归、决策树和 CatBoost）。在大多数情况下，TabDDPM 数据帮助模型取得了比其他方法更好的预测性能。
- 最后，一项分析表明，与 SMOTE 相比，TabDDPM 的特征与训练数据点没那么相似，说明它并非只是在记忆数据。（注意：基于 GAN 和 VAE 的方法未纳入这一分析。）

---

[2022 年 7 月 18 日]

### 为什么基于树的模型在表格数据上仍然优于深度学习？（2022-07）

作者：Léo Grinsztajn, Edouard Oyallon, Gaël Varoquaux

📝 论文：<https://arxiv.org/abs/2207.08815>

🖥 代码：<https://github.com/LeoGrin/tabular-benchmark>

🐦 Twitter：[解读与讨论帖](https://twitter.com/rasbt/status/1550836760128675840?s=20&t=xzoKYM9kxT_16UBA9r3LgQ)

- 主要结论是：在中等规模数据集（1 万训练样本）上，基于树的模型（随机森林和 XGBoost）优于面向表格数据的深度学习方法。
- 随着数据集规模增大（此处：1 万 -> 5 万），基于树的模型与深度学习之间的差距在缩小。
- 实验扎实，并对无信息特征的作用做了深入研究：无信息特征对深度学习方法的伤害大于对基于树的方法。
- 小小的注意事项：一些较新的表格深度学习方法未被纳入考察；"大"数据集也只有 5 万训练样本（在许多行业领域中这算小的）。
- 实验基于 45 个表格数据集：纯数值型和数值-类别混合型；涵盖分类与回归数据集；主实验使用类别均衡的 1 万训练样本；"大"数据集实验使用 5 万规模的数据集。

---

[2022 年 7 月 18 日]

### GATE：用于表格分类与回归的门控加性树集成（2022-07）

作者：Manu Joseph, Harsh Raj

📝 论文：<https://arxiv.org/abs/2207.08548>

🖥 代码：<https://github.com/manujosephv/GATE>

- 本质上，GATE 可以理解为决策树桩（decision tree stumps）的层级堆叠。
- 与 [NODE](https://arxiv.org/abs/1909.06312)（下文还会介绍）类似，所提出的 GATE 方法基于可微决策树。此外，GATE 架构受 [GRU](https://en.wikipedia.org/wiki/Gated_recurrent_unit) 门控机制启发，还包含用于（重新）加权输出的自注意力。
- 在 5 个大型数据集（3 个分类数据集和 2 个回归数据集，训练样本数从 2600 万到 8 亿）上，GATE 取得了最高的平均排名（与 LightGBM 并列）。
- 论文没有附带代码，所以我们对这些结果要有所保留。

---

[2022 年 7 月 7 日]

### 重新审视表格深度学习的[预训练](https://sebastianraschka.com/glossary/#pretraining "Pretraining")目标（2022-07）

作者：Ivan Rubachev, Artem Alekberov, Yury Gorishniy, Artem Babenko

📝 论文：<https://arxiv.org/abs/2207.03208>

🖥 代码：https://github.com/puhsu/tabular-dl-pretrain-objectives

- 与大多数基于树的方法（如梯度提升机的默认实现）不同，深度神经网络可以迭代式训练并支持预训练。本文中，作者研究了面向深度表格方法的各种预训练策略。
- 预训练在计算机视觉和自然语言处理中已是标准做法：模型在额外的（通常无标注的）数据上进行预训练。作者则改用目标数据集本身来做预训练，而不使用额外数据。
- 作者聚焦于多层感知机，研究了多种预训练方案：自预测 vs 对比方法、基于掩码的自预测 vs 重构、目标感知 vs 目标无关。
- 研究包含 11 个不同的数据集，训练样本数从 6 千到 72.3 万不等，特征数从 6 到 136。这些数据集涵盖分类与回归，以及数值特征与类别特征。
- 在大多数情况下，采用目标感知的基于掩码（自预测）预训练、并使用数值嵌入的多层感知机表现最好。只有两个数据集上梯度提升（XGBoost 和 CatBoost）胜过预训练的 MLP。

---

[2022 年 6 月 30 日]

### 使用深度表格模型进行迁移学习（2022-06）

作者：Roman Levin, Valeriia Cherepanova, Avi Schwarzschild, Arpit Bansal, C. Bayan Bruss, Tom Goldstein, Andrew Gordon Wilson, Micah Goldblum

📝 论文：<https://arxiv.org/abs/2206.15306>

🖥 代码：<https://github.com/LevinRoman/tabular-transfer-learning>

- 与梯度提升不同，面向表格数据的深度学习方法可以在上游数据上预训练，以提升在目标数据集上的性能。
- 在表格数据集情境下，有监督预训练优于自监督预训练。
- 当目标数据稀缺时，多层感知机的表现优于基于 transformer 的深度神经网络。
- 针对上游特征集与目标特征集不一致的情况，提出了一种伪特征方法。
- 使用医学诊断基准数据集：包含 11 个诊断目标的病人数据，上游数据与目标数据之间的特征相关但可能不同。

---

[2022 年 6 月 16 日]

### 借助多项式实现可扩展的可解释性（2022-06）

作者：Filip Radenovic, Abhimanyu Dubey, Dhruv Mahajan

📝 论文：<https://arxiv.org/abs/2205.14108>

🖥 代码：<https://github.com/facebookresearch/nbm-spam>

- 与[神经加性模型（NAM）](https://arxiv.org/abs/2004.13912)（下文还会介绍）类似，所提出的可扩展多项式加性模型（Scalable Polynomial Additive Models，SPAM）也是广义加性模型的一种，其主要目标是可解释性。不过，与需要为每个特征单独配备一个神经网络的 NAM 不同，SPAM 更容易扩展。
- SPAM-Neural 模型（与 NAM 共享同样的多层感知机架构）在全部 3 个表格数据集上都优于 NAM，并在 3 个案例中的 2 个上胜过 XGBoost。

---

[2022 年 6 月 1 日]

### Hopular：面向表格数据的现代 Hopfield 网络（2022-06）

作者：Bernhard Schäfl, Lukas Gruber, Angela Bitto-Nemling, Sepp Hochreiter

📝 论文：<https://arxiv.org/abs/2206.00664>

🖥 代码：<https://github.com/ml-jku/hopular>

- 提出了一种面向中小规模数据集、基于 [Hopfield 网络](https://en.wikipedia.org/wiki/Hopfield_network)（一种循环神经网络）的新深度学习架构。
- 在 21 个 UCI 数据集上，所提出的 Hopular 网络拥有最佳的中位排名（7.5）；最接近的是 [Non-Parametric Transformers](https://arxiv.org/abs/2106.02584)（11.0）。XGBoost 的中位排名为 12.0。
- 实验在 21 个 UCI 数据集上进行，样本数从 208 到 1000 不等。其中 9 个数据集还包含类别特征。
- 在《[Trouble with Hopular](https://medium.com/@tunguz/trouble-with-hopular-6649f22fa2d3)》一文中，Bojan Tunguz 指出 HistGradientBoosting 和 XGBoost 等基于树的参考方法调参不足。而经过恰当调参后，基于树的梯度提升方法会胜过所提出的 Hopular 网络。

---

[2022 年 5 月 27 日]

### 面向可解释性的神经基模型（2022-05）

📝 论文：<https://arxiv.org/abs/2205.14120>

🖥 代码：<https://github.com/facebookresearch/nbm-spam>

- 与[神经加性模型（NAM）](https://arxiv.org/abs/2004.13912)（下文还会介绍）类似，神经基模型（Neural Basis Model，NBM）也是广义加性模型的一种。与 NAM 相同，它的首要目标是可解释性。不过与 NAM 不同的是，NBM 更容易扩展，因为它是单个神经网络（而不是每个特征一个神经网络）。
- 实验包含 4 个表格数据集：1 个回归、1 个二分类和 2 个多分类数据集。数据集规模从 7 千到 40.6 万训练样本不等。
- NBM 在所有表格数据集上都优于 NAM（有 1 个数据集缺少 NAM 结果，属例外）。虽然 NBM 的预测性能明显逊于 XGBoost，但它在所有情况下都优于[可解释提升机（Explainable Boosting Machines）](https://dl.acm.org/doi/10.1145/2487575.2487579)。

---

[2022 年 3 月 15 日]

### 论表格深度学习中数值特征的嵌入（2022-03）

作者：Yury Gorishniy, Ivan Rubachev, Artem Babenko

📝 论文：<https://arxiv.org/abs/2203.05556>

🖥 代码：<https://github.com/Yura52/tabular-dl-num-embeddings>

- 作者没有为端到端学习设计新架构，而是聚焦于表格数据的嵌入方法：（1）标量值的分段线性编码；（2）基于周期激活的嵌入。
- 实验表明，这些嵌入不仅对 transformer 有益，对其他方法同样有益——在所提出的嵌入上训练时，多层感知机与 transformer 不相上下。
- 使用所提出的嵌入后，ResNet、多层感知机和 transformer 在若干（但并非全部）数据集上胜过 CatBoost 和 XGBoost。
- 小小的遗憾：我希望看到作者做一个对照实验，把所提出的嵌入也喂给 CatBoost 和 XGBoost 训练。

---

[2021 年 12 月 6 日]

### DANETs：用于表格数据分类与回归的深度抽象网络（2021-12）

作者：Jintai Chen, Kuanlun Liao, Yao Wan, Danny Z. Chen, Jian Wu

📝 论文：<https://arxiv.org/abs/2112.02962>

🖥 代码：<https://github.com/WhatAShot/DANet>

🐦 Twitter：[解读与讨论帖](https://twitter.com/rasbt/status/1564982156887310339?s=20&t=AI1HRigiz4JdvDweTD7TMg)

- DANet 架构围绕新提出的抽象层（Abstract Layer，ABSTLAY）构建，该层聚焦于两个主要步骤：1）特征选择和 2）特征抽象。
- ABSTLAY 的核心思想是（通过稀疏可学习掩码）将相关特征分组，并由此创建更高层次的抽象特征。
- 上述步骤 1 和 2 组成一个块（block），DANet 架构则由这样的块堆叠而成。
- ABSTLAY 本身由前述可学习稀疏掩码构成；此外它还有一个快捷连接（shortcut connection），把原始特征加回到每个块（这类似 ResNet 中的快捷连接，不过 ResNet 加回的是前一层的特征而非原始特征）。
- 虽然该架构无法隐式处理类别特征，但作者使用了 scikit-learn 的留一编码（leave-one-out encoding）来编码类别特征。
- 该方法在 4 个分类数据集和 3 个回归数据集上进行了评估，DANet-32 架构在 7 个数据集中的 4 个上取得了最佳性能。

---

[2021 年 10 月 5 日]

### 深度神经网络与表格数据：一篇综述（2021-10）

作者：Vadim Borisov, Tobias Leemann, Kathrin Seßler, Johannes Haug, Martin Pawelczyk, Gjergji Kasneci

📝 论文：<https://arxiv.org/abs/2110.01889>

🖥 代码：<https://github.com/kathrinse/TabSurvey>

- 一篇调研并比较面向表格数据集提出的各种深度神经网络的综述论文。
- 论文附带了基准测试代码，而且由于它*没有*提出新的表格数据方法，其结果可能比其他论文更客观。
- 根据结果，梯度提升树集成在表格数据集上仍然大多优于深度学习方法。

---

[2021 年 7 月 5 日]

### ARM-Net：面向结构化数据的自适应关系建模网络（2021-07）

作者：Shaofeng Cai, Kaiping Zheng, Gang Chen, H. V. Jagadish, Beng Chin Ooi, Meihui Zhang

📝 论文：<https://arxiv.org/abs/2107.01830>

🖥 代码：<https://github.com/nusdbsystem/ARM-Net>

- 所提出的方法把输入变换到指数空间，并使用稀疏注意力方法生成交互权重，从而获得用于预测的交叉特征。
- 这本质上是一种受 transformer 启发的嵌入方法，后接一个用于预测的多层感知机。
- 除了逻辑回归之外，论文没有包含与常规机器学习方法的比较。

---

[2021 年 6 月 29 日]

### SCARF：使用随机特征扰动的自监督对比学习（2021-06）

作者：Dara Bahri, Heinrich Jiang, Yi Tay, Donald Metzler

📝 论文：<https://arxiv.org/abs/2106.15147>

🖥 代码：N/A

- 没有公开代码，因此结果无法直接复现，需持保留态度。
- 论文提出了一种用于表格数据自监督学习的对比损失。
- 实验在 69 个分类数据集上进行，结果表明自监督方法相比纯有监督方法有所改进。

---

[2021 年 6 月 22 日]

### 重新审视面向表格数据的深度学习模型（2021-06）

📝 论文：<https://arxiv.org/abs/2106.11959>

🖥 代码：<https://github.com/Yura52/rtdl>

- 在这篇论文中，研究者讨论了表格数据深度学习文献中基线不当的问题。
- 本文的主要贡献围绕两个强基线展开：一个是类 ResNet 架构，另一个是名为 FT-Transformer（Feature Tokenizer + Transformer）的基于 transformer 的架构。
- 在本研究考虑的全部 11 个数据集上，FT-Transformer 在 6 个案例中胜过其他深度表格方法，并拥有最佳的整体排名。最具竞争力的深度表格方法是 NODE（下文还会介绍），它在 11 个案例中的 4 个里胜过其他方法。
- 与 XGBoost、CatBoost 等梯度提升树相比，FT-Transformer 在 11 个案例中的 7 个里胜出；作者的结论是不存在普遍最优的方法。

---

[2021 年 6 月 11 日]

### 调优得当的简单网络在表格数据集上表现出色（2021-06）

作者：Arlind Kadra, Marius Lindauer, Frank Hutter, Josif Grabocka

📝 论文：<https://arxiv.org/abs/2106.11189>

🖥 代码：<https://github.com/releaunifreiburg/WellTunedSimpleNets>

🐦 Twitter：[解读与讨论帖](https://twitter.com/rasbt/status/1572616437977546754?s=20&t=xzoKYM9kxT_16UBA9r3LgQ)

- 通过组合多种现代正则化技术，作者发现简单的多层感知机（MLP）可以同时胜过专用神经网络架构（TabNet）和梯度提升机（XGBoost 和 Catboost）。
- MLP 基础架构由 9 层组成，每层 512 个单元（不含输出层），并使用余弦退火调度器进行调优。
- 本研究考虑了以下 13 种正则化技术。隐式：（1）BatchNorm，（2）随机权重平均，（3）Look-ahead 优化器，（4）权重衰减。集成：（5）Dropout，（6）快照集成。结构：（7）跳跃连接，（8）Shake-Drop，（9）Shake-Shake。数据增强：（10）Mix-Up，（11）Cut-Mix，（12）Cut-Out，（13）FGSM 对抗学习。
- 比较涵盖 40 个分类表格数据集，样本数从 452 到 416,188 不等。在 40 个数据集中的 19 个上，混合使用多种正则化技术的 MLP 胜过了本研究评估的所有其他方法。
- 注意事项：作者把 NODE 纳入了比较，但没有调它的超参数。此外，正则化技术也没有应用到其他神经网络架构（TabNet 和 NODE）上。

---

[2021 年 6 月 9 日]

### XBNet：一种极度提升的神经网络（2021-06）

作者：Tushar Sarkar

📝 论文：<https://arxiv.org/abs/2106.05239>

🖥 代码：<https://github.com/tusharsarkar3/XBNet>

- 该方法的核心是利用 XGBoost 模型及其特征重要性来初始化神经网络层。
- 初始化时，它首先训练 XGBoost 模型并得到特征重要性；然后使用特征重要性来初始化多层感知机的权重。
- 初始化完成后，该方法为每个中间层额外训练一个 XGBoost 模型。因此，每一层由一个权重矩阵（对应全连接神经网络层）和一个 XGBoost 模型组成；在反向传播过程中，特征重要性被用来更新神经网络权重。
- 所提出的 XGBNet 方法在 8 个小数据集上进行了评估，其中包括经典的 Iris 和 Wine 数据集。XGBNet 在 8 个数据集中的 3 个上胜过 XGBoost。

---

[2021 年 6 月 6 日]

### 表格数据：深度学习并非你所需要的一切（2021-06）

作者：Ravid Shwartz-Ziv, Amitai Armon

📝 论文：<https://arxiv.org/abs/2106.03253>

🖥 代码：N/A

- 这篇论文比较了 XGBoost 与面向表格数据的深度学习架构；文中没有提出新方法。
- 结果显示，XGBoost 在所有数据集上的表现都优于大多数深度学习方法；不过，虽然没有任何深度学习方法能在*所有*数据集上都表现出色，但（除一个数据集之外）某个深度学习方法通常会比 XGBoost 表现更好。结论是：在不同任务上，XGBoost 的表现最为稳定。
- 另一个结论是：XGBoost 只需要少得多的超参数调优就能取得好成绩，这在许多现实场景中是一个显著优势。
- 各种集成实验值得一提：当深度神经网络与 XGBoost 结合时，取得了最佳结果。
- 论文没有提供代码示例，因此对文中的一切都要打上大大的问号。

---

[2021 年 6 月 4 日]

### 数据点之间的自注意力：超越深度学习中的单个输入-输出对（2021-06）

作者：Jannik Kossen, Neil Band, Clare Lyle, Aidan N. Gomez, Tom Rainforth, Yarin Gal

📝 论文：<https://arxiv.org/abs/2106.02584>

🖥 代码：<https://github.com/OATML/Non-Parametric-Transformers>

- 提出了一种同时处理整个数据集的深度学习方法（非参数 transformer，non-parametric transformers，NPT）。（注意，早两天上传的 [SAINT](https://arxiv.org/abs/2106.01342) 同样在行和列两个维度上做注意力。）
- 在 NPT 中，自注意力被用于数据点（行）之间以及特征（列）之间。
- 在二分类数据集上，NPT 在所有方法中拥有最佳平均排名；在多分类数据集上，NPT 与 XGBoost 打平；在回归任务上，NPT 与 XGBoost 也打成平手，但都被 CatBoost 胜过。
- 考虑数据点之间的自注意力是一种范式转变，乍看之下显得奇怪且受限。不过，对新的单个数据点做出预测是可行的，前提是训练数据集需要被用作上下文。这在某种程度上类似于 k 近邻等最近邻方法，因此也不算是全新的范式。
- 除了表格数据集，作者还在 CIFAR-10 等小图像数据集上比较了他们基于自注意力的架构。

---

[2021 年 6 月 2 日]

### SAINT：通过行注意力与对比预训练改进表格数据神经网络（2021-06）

作者：Gowthami Somepalli, Micah Goldblum, Avi Schwarzschild, C. Bayan Bruss, Tom Goldstein

📝 论文：<https://arxiv.org/abs/2106.01342>

🖥 代码：<https://github.com/somepago/saint>

- 自注意力与样本间注意力 Transformer（Self-Attention and Intersample Attention Transformer，SAINT）混合架构基于同时在行和列上施加注意力的自注意力。
- 还提出了一种在数据稀缺情况下进行预训练的自监督学习技术。
- 从全部 9 个数据集的平均性能来看，所提出的 SAINT 方法往往优于梯度提升树。这些数据集的样本数从 200 到 495,000 不等。

---

[2021 年 4 月]

### 面向表格数据的去噪自编码器（DAE）（2021-04）

📝 参考资料：[https://www.kaggle.com/competitions/tabular-playground-series-apr-2021/discussion/230013…](https://www.kaggle.com/competitions/tabular-playground-series-apr-2021/discussion/230013%E2%80%A6)

🖥 代码：<https://github.com/ryancheunggit/Denoise-Transformer-AutoEncoder>

- 该方法基于使用[去噪自编码器](https://en.wikipedia.org/wiki/Autoencoder)（Denoising Autoencoder，DAE）对表格数据进行编码，使其能被线性分类层或任何其他分类模型使用。
- 基于 DAE 的嵌入由深度神经网络产生。例如，DAE 可以基于基于 Transformer 的编码模块。
- 虽然我找不到介绍这一方法的原始文章，但它在过去几年里[赢过好几场 Kaggle 竞赛](https://www.kaggle.com/competitions/tabular-playground-series-apr-2021/discussion/230013%E2%80%A6)，例如：[Porto Seguro's Safe Driver Prediction](https://www.kaggle.com/competitions/porto-seguro-safe-driver-prediction/discussion/44629) 和 [Tabular Playground Series - Feb 2021](https://www.kaggle.com/c/tabular-playground-series-feb-2021)。（如果有人知道介绍该方法的论文，请告诉我。）

---

[2021 年 2 月 1 日]

### 将表格数据转换为图像以供卷积神经网络进行深度学习（2021-02）

作者：Yitan Zhu, Thomas Brettin, Fangfang Xia, Alexander Partin, Maulik Shukla, Hyunseung Yoo, Yvonne A. Evrard, James H. Doroshow, Rick L. Stevens

📝 论文：<https://www.nature.com/articles/s41598-021-90923-y>

🖥 代码：<https://github.com/zhuyitan/IGTD>

- 表格数据图像生成器（IGTD）在把表格数据集编码为二维图像、作为卷积网络输入这一点上，似乎采用了与 [SuperTML](https://arxiv.org/abs/1903.06246)（下文还会介绍）类似的做法。它似乎也与更早的 [TAC](https://www.biorxiv.org/content/10.1101/2020.05.02.074203v1.abstract)（TAbular Convolution）方法（同样见下文）相似。
- 有意思的是，作者没有做与 SuperTML 的比较。
- 使用 IGTD 图像的 CNN 胜过 XGBoost 和 LightGBM。

---

[2020 年 12 月 11 日]

### TabTransformer：使用上下文嵌入的表格数据建模（2020-12）

作者：Xin Huang, Ashish Khetan, Milan Cvitkovic, Zohar Karnin

📝 论文：<https://arxiv.org/abs/2012.06678>

🖥 代码：N/A

- GitHub 上有若干开源实现，但我找不到官方实现，因此对这篇论文的结果需持保留态度。
- 论文提出了一种基于自注意力、可应用于表格数据的 transformer 架构。
- 除了纯有监督模式之外，作者还提出了一种利用无监督预训练的半监督方法。
- 从 15 个数据集的平均 AUC 来看，所提出的 TabTransformer（82.8）与梯度提升树（82.9）不相上下。

---

[2020 年 6 月 5 日]

### VIME：把自监督与半监督学习的成功扩展到表格领域（2020-06）

作者：Jinsung Yoon, Yao Zhang, James Jordon, Mihaela van der Schaar

📝 论文：<https://proceedings.neurips.cc/paper/2020/hash/7d97667a3e056acab9aaf653807b4a03-Abstract.html>

🖥 代码：<https://github.com/jsyoon0823/VIME>

- VIME（Value Imputation and Mask Estimation，值插补与掩码估计）包含面向表格数据的自监督和半监督学习框架。
- 作者提供了不错的消融实验，表明 VIME 的半监督变体优于纯有监督和纯自监督变体。最佳 VIME 变体同时使用自监督和半监督学习，在所有数据集上都胜过 XGBoost。
- 该比较仅基于五个数据集。

---

[2020 年 5 月 3 日]

### 一种使用卷积神经网络进行表格数据分类的新方法（2020-05）

作者：Ljubomir Buturović, Dejan Miljković

📝 论文：<https://www.biorxiv.org/content/10.1101/2020.05.02.074203v1.abstract>

🖥 代码：N/A

- 与 [SuperTML](https://arxiv.org/abs/1903.06246)（见下文）类似，该方法把表格数据转换为图像格式，作为面向图像数据的常规卷积神经网络的输入。
- 研究者把该方法应用于一个基因分类数据集。他们发现 TAC 方法（91.1% 准确率）略优于其他非深度学习方法：线性 SVM（89.6% 准确率）、XGBoost（87.6% 准确率）等。
- TAC 是在多个图像数据集的组合上预训练后才达到这一性能的——论文没有提供不带预训练的 TAC 基线。
- 论文没有附带代码，所以对这些结果要有所保留。

---

[2020 年 4 月 29 日]

### 神经加性模型：用神经网络做可解释机器学习（2020-04）

📝 论文：<https://arxiv.org/abs/2004.13912>

🖥 代码：<https://github.com/google-research/google-research/tree/master/neural_additive_models>

- 所提出的神经加性模型（Neural Additive Models，NAM）本质上是多层感知机（MLP）的集成；这里每个输入特征使用一个 MLP。
- 每个 MLP 恰好有一个输入节点和一个输出节点，但可以有任意数量的隐藏层和节点。输出值随后被求和，并传入 logistic sigmoid 函数用于二分类。（对于回归，可以省略 sigmoid 激活。）
- 该方法的主要优点是易于解释，因为每个输入特征都由一个独立的神经网络处理；也就是说，每个特征对总输出（按简单求和计算）的贡献都可以轻松评估。
- NAM 在 4 个数据集（2 个分类和 2 个回归）上进行了评估。虽然它在全部 4 个数据集上都略逊于 XGBoost，但在 4 个数据集中的 2 个上优于[可解释提升机（Explainable Boosting Machines）](https://dl.acm.org/doi/10.1145/2487575.2487579)。

---

[2019 年 9 月 13 日]

### 面向表格数据深度学习的神经健忘决策集成（2019-09）

作者：Sergei Popov, Stanislav Morozov, Artem Babenko

📝 论文：<https://arxiv.org/abs/1909.06312>

🖥 代码：<https://github.com/Qwicen/node>

- 所提出的神经健忘决策集成（Neural Oblivious Decision Ensembles，NODE）方法把决策树与深度神经网络结合起来，使其能够以端到端的方式（通过基于梯度的优化）训练。
- 该方法基于所谓的健忘决策树（oblivious decision trees，ODT），这是一种特殊的决策树，"在同一深度的所有内部节点中使用相同的分裂特征和分裂阈值"。
- 实验在 6 个大型数据集上进行，训练样本数从 40 万到 1050 万不等。
- 使用默认超参数时，NODE 在全部 6 个数据集上都略微胜过 XGBoost；调优超参数后，NODE 在 6 个案例中的 4 个里胜过 XGBoost。
- 使用 1080Ti GPU 时，NODE 的训练速度（7 分 42 秒）比 XGBoost（1 分 13 秒）慢约 7 倍；推理时，NODE（8.56 秒）比 XGBoost（4.45 秒）慢约 2 倍。

---

[2019 年 8 月 20 日]

### TabNet：注意力式可解释表格学习（2019-08）

作者：Sercan O. Arik, Tomas Pfister

📝 论文：<https://arxiv.org/abs/1908.07442>

🖥 代码：<https://github.com/google-research/google-research/tree/master/tabnet>

- 根据我的个人经验，TabNet 是第一个获得广泛"关注"的表格数据深度学习架构（无意双关）。
- TabNet 基于一种顺序注意力机制，并表明在表格场景中，利用无标注数据的自监督学习可以超越纯有监督训练模式。
- 在 6 个合成数据集上，TabNet 在 6 个案例中的 3 个里胜过其他方法。不过，实验中省略了 XGBoost，基于树的参考方法是[极端随机树](https://link.springer.com/article/10.1007/s10994-006-6226-1)而非随机森林。
- 在 4 个 KDD 数据集上，TabNet 在其中 1 个数据集上与 CatBoost 和 XGBoost 打平，在其余三个数据集上的表现几乎与梯度提升树方法一样好。

---

[2019 年 2 月 26 日]

### SuperTML：用于结构化表格数据预测的二维词嵌入（2019-02）

作者：Baohua Sun, Lin Yang, Wenhan Zhang, Michael Lin, Patrick Dong, Charles Young, Jason Dong

📝 论文：<https://arxiv.org/abs/1903.06246>

🖥 代码：无官方实现

- 所提出的 SuperTML 方法从表格数据创建二维（类图像）嵌入。
- 这些二维嵌入随后被用作常规卷积神经网络的输入。
- SuperTML 方法在全部三个数据集上都胜过 XGBoost：Iris（150 样本）、Wine（178 样本）和 Adult（48,842 样本）。
- 注意：所选数据集非常有限。
- 虽然 GitHub 上有几个实现，但没有作者的官方实现，因此结果不容易复现。

---

## 工具与基准测试

至于具体方法的代码实现，我建议参考大多数论文随附的官方代码仓库。不过，还有一些专门的工具和库值得一提。

- [AutoGluon](https://auto.gluon.ai/stable/index.html)（参见 `autogluon.tabular`）：一个用于堆叠集成神经网络的库；使用 PyTorch 实现。
- [PyTorch-Tabular](https://pytorch-tabular.readthedocs.io/en/latest/)：一个实现了 5 种深度表格方法的 PyTorch 库（截至撰写时，2022 年 9 月）。
- [Auto-PyTorch](https://github.com/automl/Auto-PyTorch)：一个面向表格数据集的基于 PyTorch 的神经架构搜索库。
- [PyTorch-widedeep](https://github.com/jrzaurin/pytorch-widedeep)：一个灵活的多模态深度学习包，在 PyTorch 中使用 Wide and Deep 模型把表格数据与文本和图像结合起来。
- [TabularBenchmarks](https://github.com/tunguz/TabularBenchmarks/tree/main/datasets)：由 Bojan Tunguz 维护的一套相当有代表性的表格数据数据集与基准测试合集（目前仍是草稿）。

## 结语

就个人而言，我觉得在表格数据集上使用深度学习算法的想法既怪异又有趣。这或许是因为我对总是使用同样的方法感到有些厌倦。别误会，这些方法是有效的，但我也喜欢动手折腾，喜欢尝试新事物。

你应该在表格数据集上使用深度学习吗？大概率不必。不过这也可能取决于你是否富有冒险精神、是否有一些可以"浪费"的时间。

我的建议始终是：先从一个可靠的基线开始。我会先选随机森林。然后，我会尝试 scikit-learn 中的 HistGradientBoosting（一个受 LightGBM 启发、强大且易用的梯度提升实现）。如果效果不错而且你还有富余时间，我强烈推荐试试 XGBoost。只有当你还有更多富余时间、想搞点实验、并且喜欢折腾时，我才会在表格数据集上尝试深度学习方法。
