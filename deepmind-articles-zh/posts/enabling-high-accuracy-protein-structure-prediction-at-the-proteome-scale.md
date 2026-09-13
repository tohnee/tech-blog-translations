---
title: "在蛋白质组尺度上实现高精度蛋白质结构预测"
title_en: "Enabling high-accuracy protein structure prediction at the proteome scale"
source: https://deepmind.google/blog/enabling-high-accuracy-protein-structure-prediction-at-the-proteome-scale/
site: deepmind
date: 2021-07-22
crawled: 2026-09-13
translated: 2026-09-13
---

# 在蛋白质组尺度上实现高精度蛋白质结构预测

> 原文：[Enabling high-accuracy protein structure prediction at the proteome scale](https://deepmind.google/blog/enabling-high-accuracy-protein-structure-prediction-at-the-proteome-scale/) · Google DeepMind

## AlphaFold 方法

许多新颖的机器学习创新共同造就了 AlphaFold 目前的精度水平。我们在下面对该系统做一个高层概览；有关网络架构的技术描述，请参阅我们的 AlphaFold [方法论文](https://www.nature.com/articles/s41586-021-03819-2)，尤其是其中内容详尽的补充材料。

AlphaFold 网络由两个主要阶段组成。第一阶段以氨基酸序列和多序列比对（MSA）作为输入，其目标是学习一个丰富的「成对表示」，该表示能提供关于哪些残基对在 3D 空间中彼此接近的信息。

第二阶段利用这一表示直接生成原子坐标：它将每个残基视为一个独立对象，预测放置每个残基所需的旋转与平移，最终组装出结构化的链。网络的设计汲取了我们关于蛋白质物理与几何的直觉，例如体现在所应用的更新形式以及损失函数的选择上。

有趣的是，我们可以基于网络中间层的表示生成 3D 结构。由此得到的「轨迹」视频展示了在推理过程中，AlphaFold 对正确结构的信念如何逐层形成。通常，一个假设会在前几层之后浮现，随后经历漫长的精化过程；不过有些目标需要用到网络的全部深度才能得到良好的预测。

![动态 3D 轨迹视频：展示 AlphaFold 预测的蛋白质结构在推理过程中如何逐层生成和精化，从一个粗糙的假设逐步演变为高度结构化的多色链。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_1_BeVC9fP.gif)

![动态 3D 轨迹视频：展示 AlphaFold 预测的蛋白质结构在推理过程中如何逐层生成和精化，从一个粗糙的假设逐步演变为高度结构化的多色链。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_2_6UHmi8M.gif)

![动态 3D 轨迹视频：展示 AlphaFold 预测的蛋白质结构在推理过程中如何逐层生成和精化，从一个粗糙的假设逐步演变为高度结构化的多色链。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fig_3_6Ul0Gch.gif)

CASP14 目标 T1044、T1024 和 T1064 在网络相继各层上的预测结构。结构按残基序号着色，计数器显示当前层。

## 精度与置信度

AlphaFold 在 [CASP14](https://predictioncenter.org/casp14/zscores_final.cgi) 评测中接受了严格评估，参赛者需要盲测预测那些已被解析但尚未公开的蛋白质结构。该方法在大多数案例中都达到了很高的精度，对实验结构的平均 95% RMSD-Cα 小于 1 埃。在论文中，我们进一步在规模大得多的近期 PDB 条目集合上评估了该模型。发现包括：在大型蛋白质上表现强劲，并且在主链预测良好的情况下侧链精度也很高。

![条形图：显示 AlphaFold 在 CASP14 上的精度相对于 Tfold_Human、Baker、Zhang、Baker experimental 等其他方法的表现。](https://lh3.googleusercontent.com/w0ugEc2xzlJObbTQh51BMG153ONu_3lEsbxr9eLKDX7hEUF7Pqh1pNUaE1guX8TA8gKsGhgaoLA5g3sjcuA2287A37_gIDgzn8q4Nky_DvlxWHtkgeQ=w1440)

AlphaFold 在 CASP14 上的精度与其他方法的对比。RMSD-Cα 基于每个目标中预测最好的 95% 残基计算。

结构预测实用价值的一个重要因素是相关置信度指标的质量。模型能否识别其预测中可能可靠的部分？为此，我们在 AlphaFold 网络之上开发了两个置信度指标。

第一个是 pLDDT（[predicted lDDT-Cα](https://doi.org/10.1093/bioinformatics/btt473)），这是一个按残基计算的局部置信度指标，取值范围为 0 到 100。pLDDT 沿链的分布可能变化剧烈，使模型能够对结构化结构域表达高置信度，而对结构域之间的连接区域表达低置信度。在我们的[论文](https://www.nature.com/articles/s41586-021-03828-1)中，我们给出证据表明，某些 pLDDT 较低的区域在单独存在时可能是无结构的——要么是内在无序的，要么只在更大复合物的语境中才有结构。pLDDT < 50 的区域不应作其他解读，只能视为一种可能的无序预测。

第二个指标是 PAE（Predicted Aligned Error，预测对齐误差），它报告当预测结构与真实结构在残基 y 上对齐时，AlphaFold 在残基 x 处的预期位置误差。这对于评估全局特征（尤其是结构域堆积）的置信度很有用。对于来自两个不同结构域的残基 x 和 y，(x, y) 处持续偏低的 PAE 表明 AlphaFold 对结构域的相对位置很有信心；而 (x, y) 处持续偏高的 PAE 则表明结构域的相对位置不应作解读。生成 PAE 所用的通用方法还可以适配用于预测多种基于叠合的指标，包括 [TM-score](https://doi.org/10.1002/prot.20264) 和 [GDT](https://doi.org/10.1093/nar/gkg571)。

![示意图：展示 AlphaFold 的置信度指标。左侧为两个按逐残基置信度（pLDDT）着色的预测蛋白质结构，蓝色表示高/中置信度，橙色表示低/极低置信度。右侧为两个预测对齐误差（PAE）热图：上方热图展示"相对位置不确定"的情况，局部深绿色方块表明单个结构域定义良好但结构域间缺乏置信度；下方热图展示"相对位置可信"的情况，大片绿色区块表明对结构域全局相对排布具有高置信度。](https://lh3.googleusercontent.com/g__7WFe_n5sioMoF0oIAPVVFkNHPA5T5T5Rcd1VdTBOzUoQqZ3szE-LjuZPJmg_llUFsoRUtvUX3XrmKb74S1cK44l8GjMMlrUpMQvvFf5jKkRb1z2I=w1440)

两个示例蛋白质（P54725、Q5VSL9）的逐残基置信度（pLDDT）与预测对齐误差（PAE）。两者都有可信的独立结构域，但后者还具有可信的结构域相对位置。注：Q5VSL9 的结构是在该预测生成之后才被解析的。

需要强调的是，AlphaFold 模型归根结底是预测：虽然常常高度准确，但有时也会出错。预测的原子坐标应谨慎解读，并结合上述置信度指标进行理解。

## 开源

与方法论文一同，我们已在 [GitHub](https://github.com/deepmind/alphafold) 上公开了 AlphaFold 的源代码。其中包括一个训练好的模型的访问权限，以及一个用于对新的输入序列进行预测的脚本。我们相信这是重要的一步，将使社区能够使用我们的工作并在此基础上继续构建。使用 AlphaFold 折叠单个新蛋白质最简单的方式是使用我们的 [Colab notebook](https://bit.ly/alphafoldcolab)。

开源代码是基于 [JAX 框架](https://github.com/google/jax)的 CASP14 系统的更新版本，达到了同样高的精度。它还纳入了一些近期的性能改进。AlphaFold 的速度一直在很大程度上取决于输入序列的长度：短蛋白质只需几分钟即可处理完，只有非常长的蛋白质才需要数小时。现在，一旦 MSA 组装完成，开源版本只需在 V100 上约一分钟的 GPU 时间，即可预测出一个 400 残基蛋白质的结构。

## 蛋白质组尺度与 AlphaFold DB

AlphaFold 的快速推理使该方法能够应用于全蛋白质组尺度。在[论文](https://www.nature.com/articles/s41586-021-03828-1)中，我们讨论了 AlphaFold 对人类蛋白质组的预测。此后，我们还为许多[模式生物、病原体以及具有经济意义的物种](https://alphafold.ebi.ac.uk/download)的参考蛋白质组生成了预测，大规模预测如今已成为常规操作。有趣的是，我们观察到不同物种之间 pLDDT 分布存在差异：细菌和古菌上的置信度普遍较高，而真核生物上的置信度较低，我们推测这可能与这些蛋白质组中无序区域的普遍程度有关。

没有任何一个研究团队能够充分探索如此庞大的数据集，因此我们与 [EMBL-EBI](https://www.ebi.ac.uk/) 合作，通过 [AlphaFold DB](https://alphafold.ebi.ac.uk/) 免费公开这些预测。每个预测都可以与上述置信度指标一同查看。我们还为每个物种提供了批量下载，所有数据均采用 CC-BY-4.0 许可（使其可免费用于学术和商业用途）。我们极其感谢 EMBL-EBI 与我们共同开发这一新资源所做的工作。在接下来的几个月中，我们计划将数据集扩展到覆盖 [UniRef90](https://www.uniprot.org/uniref/?query=&fil=identity:0.9) 中超过一亿个蛋白质。

![3x3 网格：展示 AlphaFold 为不同参考蛋白质组（包括裂殖酵母、秀丽隐杆线虫、结核分枝杆菌、芽殖酵母、果蝇、恶性疟原虫、拟南芥、盘基网柄菌和大肠杆菌）预测的各种 3D 蛋白质结构，按逐残基预测置信度（pLDDT）着色，从高置信度（蓝色）到低置信度（橙色）。](https://lh3.googleusercontent.com/GqFl_KlLOJ6EmtNLXYYTKQFT1lwT3OFPy_jrEkKzEyB6cFRcrqcg8VC3dDtYzSZ7AzkPJEA4V98UHq7WWHpUhiJUNqMyQOmDoQJnF1fKVzJyM3lh=w1440)

示例：来自多种生物的 AlphaFold DB 预测。

![三幅 3D 山脊图：展示 AlphaFold 逐残基预测置信度（pLDDT）在十五个参考蛋白质组中的分布。真核生物蛋白质组（中、右）普遍显示较低的置信度和更高比例的低置信度区域，而细菌和古菌蛋白质组（左）在接近 100% 置信度处呈现尖锐峰。](https://lh3.googleusercontent.com/VaeRpgcBDCr-tB8f42iE4cXy0tTjghF9lYoqL3aTau-fgS5YAkaj74IFaj-tifz2kErEIlNa1KVkVICfVSfZvL7Co4wqD1Jj56pT5665cmUJgp1Fs70=w1440)

14 个物种的逐残基置信度分布；从左到右：细菌/古菌、动物和原生生物。

在 AlphaFold DB 中，我们选择共享长度不超过 2700 个氨基酸的完整蛋白质链的预测，而不是裁剪为单个结构域。理由是这样可以避免遗漏尚未被注释的结构化区域，同时提供完整氨基酸序列的上下文，并允许模型尝试结构域堆积预测。AlphaFold 的结构域内精度在 CASP14 中得到了更充分的评估，预计会高于其结构域间精度。不过，AlphaFold 在结构域间评估中排名第一，我们预计它在某些情况下仍能给出有参考价值的预测。我们建议用户查看 PAE 图，以判断结构域的摆放是否可能有意义。

## 未来工作

我们对计算结构生物学的未来感到兴奋。仍有许多重要课题有待解决：预测复合物的结构、纳入非蛋白质组分、捕捉动力学以及对点突变的响应。像 AlphaFold 这样在理解蛋白质结构任务上表现出色的网络架构的发展，让我们有理由乐观地认为可以在相关问题上取得进展。

我们将 AlphaFold 视为实验结构生物学的互补技术。这一点也许在它帮助解析实验结构方面体现得最为明显，包括通过分子置换以及向冷冻电镜密度图中的对接。这两种应用都能加速现有研究，节省数月的精力。从生物信息学的角度看，AlphaFold 的速度支持大规模生成预测结构，这有望通过支持对大型序列数据库内容的结构研究，开辟新的研究途径。

最终，我们希望 AlphaFold 能被证明是照亮蛋白质空间的有用工具，并期待在未来的几个月和几年里看到它被如何应用。

我们非常乐意听取你的反馈，了解 AlphaFold 和 AlphaFold DB 如何对你的研究有所帮助。欢迎在 [alphafold@deepmind.com](mailto:alphafold@deepmind.com) 分享你的故事。
