---
title: "通过规模解锁高精度的差分隐私图像分类"
title_en: "Unlocking High-Accuracy Differentially Private Image Classification through Scale"
source: https://deepmind.google/blog/unlocking-high-accuracy-differentially-private-image-classification-through-scale/
site: deepmind
date: 2022-06-17
crawled: 2026-09-13
translated: 2026-09-13
---

# 通过规模解锁高精度的差分隐私图像分类

> 原文：[Unlocking High-Accuracy Differentially Private Image Classification through Scale](https://deepmind.google/blog/unlocking-high-accuracy-differentially-private-image-classification-through-scale/) · Google DeepMind

DeepMind 最近一篇[关于语言模型伦理与社会风险的论文](https://arxiv.org/abs/2112.04359)指出，大语言模型[泄露训练数据中的敏感信息](https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting)是一种潜在风险，从事这类模型研究的机构有责任加以解决。另一篇[近期论文](https://arxiv.org/abs/2201.04845)表明，类似的隐私风险也可能出现在标准图像分类模型中：每张训练图像的"指纹"都会被嵌入模型参数之中，恶意方可以利用这些指纹从模型中重建训练数据。

差分隐私（differential privacy，DP）等隐私增强技术可以在训练时部署以缓解这些风险，但它们往往会导致模型性能显著下降。在这项工作中，我们在"以差分隐私实现高精度图像分类模型训练"的方向上取得了实质性进展。

![机器学习模型中隐私风险的示意图：左侧为 GPT-2 中的文本记忆现象，右侧为从标准图像分类模型中成功重建的训练图像。](https://lh3.googleusercontent.com/EE-e4w3q5sqP90b5wMttB0k5SW6fiJ-9xEp6lBcGYglzX-7gIyhq5x3GOXEOHf9derEkSjSQY4TrF_lPmCnBat79uetL5p7ta5KZFJQF9j840EdN2dg=w1440)

图 1：（左）GPT-2 训练数据泄露的图示［来源：Carlini 等，"Extracting Training Data from Large Language Models"，2021］。（右）从 10 万参数卷积神经网络重建出的 CIFAR-10 训练样例［来源：Balle 等，"Reconstructing Training Data with Informed Adversaries"，2022］

差分隐私最初是作为一套数学框架被[提出的](https://link.springer.com/content/pdf/10.1007/11681878_14.pdf)，用于刻画在统计分析（包括机器学习模型的训练）过程中保护个体记录的需求。DP 算法通过在计算所需统计量或模型的过程中注入经过仔细校准的噪声，防止他人对个体的独特特征做出任何推断（包括完整或部分重建）。使用 DP 算法在理论和实践中都能提供强健而严格的隐私保证，并已成为众多[公共](https://dl.acm.org/doi/10.1145/3219819.3226070)与[私营](https://ai.googleblog.com/2022/02/federated-learning-with-formal.html)机构采用的事实上的黄金标准。

深度学习中最常用的 DP 算法是差分隐私随机梯度下降（DP-SGD），它是对标准 SGD 的改进：对每个样例的梯度进行裁剪，并加入足够的噪声以掩盖任何单个样本对每次模型更新的贡献。

![差分隐私随机梯度下降（DP-SGD）训练循环示意图：训练数据被送入模型以计算每个样例的梯度，这些梯度经过裁剪、平均并与加入的噪声结合生成隐私化梯度，随后用于更新模型参数。](https://lh3.googleusercontent.com/jPzWgyDsXg_xXncwyZZhqKWrH39Seck6BVmdLyT6nbIMKjdBiFwpkXXHFh8b_rtvPpISyzu7smCRg_-5gtG21Ax_Uzaabf-Xx6JXcFtw60zKGbwpRQ=w1440)

图 2：DP-SGD 处理单个样例梯度并加入噪声、以带隐私化梯度产生模型更新的示意图。

遗憾的是，先前的研究发现，在实践中 DP-SGD 提供的隐私保护往往以模型精度显著下降为代价，这成为机器学习界广泛采用差分隐私的一大障碍。先前工作的经验证据表明，DP-SGD 的这种性能退化在更大的神经网络模型上更为严重——包括那些通常用于在具有挑战性的图像分类基准上取得最佳性能的模型。

我们的工作研究了这一现象，并对训练过程和模型架构提出了一系列简单的修改，使标准图像分类基准上的 DP 训练精度得到了显著提升。我们研究中最令人惊讶的发现是：只要确保模型的梯度表现良好，DP-SGD 就能高效训练比以往认知中深得多的模型。我们相信，我们的研究所取得的性能跃升，有望解锁带有正式隐私保证的图像分类模型的实际应用。

下图总结了我们的两个主要结果：在不使用额外数据的隐私化训练中，CIFAR-10 上的准确率比先前工作提升了约 10%；在对一个在其他数据集上预训练的模型进行隐私化微调时，ImageNet 上的 top-1 准确率达到 86.7%，几乎抹平了与非隐私最佳性能之间的差距。

![两张柱状图展示论文在 ε=8 下的结果。在不使用额外数据的 CIFAR-10 上，"我们的方法"取得 81.4% 的 top-1 准确率，相比之下"此前最佳结果"为 71.7%。在 ImageNet 微调上，"我们的方法"取得 86.7% 的 top-1 准确率，接近非隐私的最先进（SOTA）水平 91%。](https://lh3.googleusercontent.com/lsVsbIezoFPBKTvpRzIFU3sxI8g_ajbrzqaR2WbpBukTBuYkFS0_pC6mBC3OOTM4E55R7M4pg_s7NZTUO7seK-x5-54axMx8MqW9oCxzyhzCcWLeCQ=w1440)

图 3：（左）在不使用额外数据的情况下在 CIFAR-10 上训练 WideResNet 模型的最佳结果。（右）在 ImageNet 上微调 NFNet 模型的最佳结果。表现最好的模型在与 ImageNet 不相交的内部数据集上进行了预训练。

这些结果是在 ε=8 下取得的——这是校准差分隐私在机器学习应用中保护强度的一个标准设置。关于这一参数的讨论，以及在其它 ε 值和其他数据集上的更多实验结果，请参见论文。连同论文一起，我们也开源了我们的实现，以便其他研究人员验证我们的发现并在此基础上继续发展。我们希望这一贡献能帮助那些希望让实用 DP 训练成为现实的人们。

在 [GitHub](https://github.com/deepmind/jax_privacy) 上下载我们的 JAX 实现。
