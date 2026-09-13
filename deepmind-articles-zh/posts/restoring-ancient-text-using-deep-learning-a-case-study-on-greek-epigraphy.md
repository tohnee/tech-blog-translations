---
title: "用深度学习修复古代文本：希腊碑铭学案例研究"
title_en: "Restoring ancient text using deep learning: a case study on Greek epigraphy"
source: https://deepmind.google/blog/restoring-ancient-text-using-deep-learning-a-case-study-on-greek-epigraphy/
site: deepmind
date: 2019-10-15
crawled: 2026-09-13
translated: 2026-09-13
---

# 用深度学习修复古代文本：希腊碑铭学案例研究

> 原文：[Restoring ancient text using deep learning: a case study on Greek epigraphy](https://deepmind.google/blog/restoring-ancient-text-using-deep-learning-a-case-study-on-greek-epigraphy/) · Google DeepMind

历史学家依靠各种不同的史料来重建过往文明的思想、社会与历史。这些史料中有许多是以文本形式存在的——无论是写在卷轴上还是刻在石头上，这些留存下来的过往记录都有助于揭示古代社会的面貌。然而，这些古代文化遗产的记录往往并不完整：或是由于人为的毁坏，或是由于岁月的侵蚀与破碎。碑铭（inscriptions）正是如此——它们是过去的个人、群体和机构书写在耐久表面（如石头、陶器、金属）上的文字，也是一门被称为[碑铭学（epigraphy）](https://en.wikipedia.org/wiki/Epigraphy)的学科的研究对象。数以千计的碑铭留存至今，但其中大多数在漫长世纪中遭到损坏，文本的一部分已无法辨认或彻底佚失（图 1）。修复（「复原」）这些文献复杂而耗时，但却是更深入理解过往文明所必需的。

从不完整的文本片段中辨析含义，其难点之一在于往往存在多种可能的答案。在许多文字游戏和字谜中，玩家需要猜测字母来补全一个单词或短语——被指定的字母越多，可能的答案范围就越受约束。但与这些玩家孤立地猜测一个短语的游戏不同，修复文本的历史学家可以根据碑铭中的其他上下文线索来估计不同可能答案的可能性——例如语法和语言学方面的考量、排版与形状、文本平行例证以及历史背景。如今，通过使用以古代文本训练的机器学习，我们构建了一个系统，它能够提供一份更完整、经系统排序的可能答案列表，我们希望这能增进历史学家对文本的理解。

![一块受损且碎裂的古代石板照片，上面刻有希腊语铭文，展示了修复不完整历史文本所面临的挑战。](https://lh3.googleusercontent.com/6St-mHlvrbnx-TxQDdp4AaznvkIlsm796RI7l4prcpdjvvq-lde7ZdFiB_C8UTmDkEm9xUsaDUcV9rD6ilqG_T1jTiklcs3xGKJwuwfIwb9lsaE_8A=w1440)

图 1：受损的碑铭：雅典公民大会关于卫城管理的一项法令（年代为公元前 485/4 年）。IG I3 4B。（CC BY-SA 3.0，WikiMedia）

## Pythia

Pythia——得名于在希腊德尔斐圣所为神明阿波罗传达神谕的女祭司——是首个利用深度神经网络从受损文本输入中恢复缺失字符的古代文本修复模型。这项工作将古代历史与深度学习两个学科结合在一起，为文本修复任务提供了一个全自动的辅助工具，为古代历史学家提供多个文本复原方案，以及每个假设的置信水平。

Pythia 以一段受损的文本序列作为输入，经过训练来预测字符序列，构成对古希腊碑铭（以希腊字母书写、年代介于公元前七世纪至公元五世纪之间的文本）的假设性复原。该架构同时在字符级和词级上工作，从而能够有效处理长期上下文信息，并高效应对不完整的词表示（图 2）。这使它适用于所有研究古代文本的学科（[文献学](https://en.wikipedia.org/wiki/Philology)、[纸草学](https://en.wikipedia.org/wiki/Papyrology)、[抄本学](https://en.wikipedia.org/wiki/Codicology)），并可应用于任何语言（古代或现代）。

![Pythia 神经网络架构示意图，展示了字符嵌入和词嵌入——包括以红色问号标注的缺失字符——如何经过带有注意力机制的编码器状态进行解码，并预测出缺失的希腊字母「γ」和「α」。](https://lh3.googleusercontent.com/ZeGSNfVOO6Qn4OPmLCh_8tQC5zH7A0m4f2Ut4bQoEAap58Bky9keEiiYgU4DgtNH3USXMw79_GaLIaEeCnTKpEQSAwjpZLK1TzPRmAaCnZdgZR_62Q=w1440)

图 2：Pythia 处理短语 μηδέν ἄγαν（Mēdèn ágan，「凡事勿过度」）——这句刻在德尔斐阿波罗神庙上的著名格言。字母「γα」是待预测的字符，以「?」标注。由于 ἄ??ν 不是一个完整的词，其嵌入被当作未知（'unk'）处理。解码器正确输出了「γα」。

## 实验评估

为了训练 Pythia，我们编写了一条非同寻常的处理流水线，将最大的古希腊碑铭数字语料库（[PHI Greek Inscriptions](https://epigraphy.packhum.org/)）转换为机器可处理的文本，我们称之为 PHI-ML。如表 1 所示，Pythia 在 PHI-ML 上的预测字符错误率为 30.1%，而接受评估的人类古代历史学家（具体而言，是来自牛津大学的博士生）的字符错误率为 57.3%。此外，在 73.5% 的案例中，真实文本序列位列 Pythia 的 Top-20 假设之中，这有力地证明了这种辅助方法对数字碑铭学领域的影响，并树立了古代文本修复领域的最新技术水准。

![表 1：古代文本修复方法的对比，展示字符错误率（CER）和 Top-20 准确率。其中 Pythia-Bi-Word 取得最低的 30.1% 字符错误率和最高的 73.5% Top-20 准确率，而古代历史学家的字符错误率为 57.3%。](https://lh3.googleusercontent.com/PrVvoB5lHweiZaiyCuboLb4Dl6PBVvUKwGWLJC1DaQJy7qWx7hC-UdcMulMla7_Y1TpzUT4-5AGuaQoGCJnbWlsWjuMAe-h8PvCfzNKExWR_BoJMLQ=w1440)

表 1：Pythia 在 PHI-ML 上的预测性能。

## 上下文的重要性

为了评估 Pythia 对上下文信息的敏感程度，并可视化每个解码步骤的注意力权重，我们用来自帕加马城（位于今土耳其境内）的一方碑铭的修改行做了实验\*。在图 3 的文本中，最后一个词是一个以 -ου 结尾的希腊人名。我们设定 ἀπολλοδώρου（"Apollodorou"）为人名，并将其前 9 个字符隐藏。特意选择这个名字，是因为它已经出现在输入文本中。Pythia 的注意力聚焦于文本中与上下文相关的部分——具体来说就是 ἀπολλοδώρου。序列 ἀπολλοδώρ 被正确预测。作为一次「石蕊测试」，我们把输入文本中的 ἀπολλοδώρου 替换为另一个同样长度的希腊人名：ἀρτεμιδώρου（"Artemidorou"）。预测序列也随之变为 ἀρτεμιδώρ，从而说明了上下文在预测过程中的重要性。

![Pythia 在四个解码步骤中的注意力权重可视化：它根据「Apollodorou」在上下文中的先前出现，预测以问号表示的缺失希腊字符。](https://lh3.googleusercontent.com/cW3PAl3WIEyX8rz_GCSscSWFj86CBaBj7B3gK2r8bEAU7vTFOQ45g7kSO_7Gj7FNMDGTnc9Yt25XVXeELyWTLZZa1uovntW6uhO5W-TAncFRXRbT=w1440)

图 3：解码前 4 个缺失字符的注意力权重可视化。为了便于观察，待预测字符（'?'）区域内的权重以绿色显示，文本其余部分以蓝色显示；权重大小以颜色深浅表示。真实文本 ἀπολλοδώρ 出现在输入文本中，Pythia 的注意力集中在序列的相关部分。

## 未来研究

机器学习与碑铭学的结合，有潜力对碑铭文本的研究产生实质性影响，并拓宽历史学家工作的范围。为此，我们已将在线 Python notebook Pythia 以及 PHI-ML 的处理流水线开源至 <https://github.com/sommerschield/ancient-text-restoration>，并与牛津大学的学者展开合作。我们希望借此助力未来的研究，并激发更多跨学科工作。

**注释**

\*具体而言，是碑铭 MDAI(A) 32 (1907) 428, 275 的第 b.8–c.5 行。
