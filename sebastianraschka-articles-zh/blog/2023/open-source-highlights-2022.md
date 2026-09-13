---
title: "2022 年机器学习与 AI 开源项目亮点"
title_en: "ML & AI Open Source Highlights 2022"
source: https://sebastianraschka.com/blog/2023/open-source-highlights-2022.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 2022 年机器学习与 AI 开源项目亮点

> 原文：[ML & AI Open Source Highlights 2022](https://sebastianraschka.com/blog/2023/open-source-highlights-2022.html)

最近，我[分享了 2022 年我读过的十佳论文](https://magazine.sebastianraschka.com/p/ahead-of-ai-4-a-big-year-for-ai)。作为后续，我在整理一份我最喜欢的 10 个开源项目清单——都是我在 2022 年发现、使用或参与贡献的项目。

（注意，各小节的编号不代表任何排名或偏好。有些库之间存在某种关联，我按推荐阅读顺序排列了这些小节。）

## 1) 宣布支持图编译的 PyTorch 2.0

先从我每天都在用的深度学习库说起：PyTorch！

PyTorch 团队上个月在 [PyTorch Conference 2022](https://pytorch.org/blog/announcing-pytorch-conference-2022/) 上宣布了 PyTorch 2.0。好消息是核心 API 不会变，重点将放在让 PyTorch 更高效上。

此外，PyTorch 团队正在把一些代码从 C++ 移到 Python，使其对开发者更友好。总体而言，这些更新旨在让 PyTorch 更加易用。

[![pytorch2](https://sebastianraschka.com/images/blog/2023/open-source-highlights-2022/pytorch2.webp)](https://pytorch.org/get-started/pytorch-2.0/)

PyTorch 2.0 专注于底层改动，其中包括可选的新函数 `torch.compile`，用于图编译以提升模型效率。将来，可以用 `torch.compile` 包裹整个训练循环。当然，用户仍可以继续以 eager 模式使用 PyTorch。

`torch.compile` 已经可以通过 PyTorch nightly 版本使用，并将包含在即将发布的 PyTorch 版本中。想试试吗？只需要一行代码：

```python
compiled_model= torch.compile(model)
```

PyTorch 2.0 的稳定版计划于 2023 年 3 月发布。在此期间，你可以在[这里](https://pytorch.org/get-started/pytorch-2.0/)找到 PyTorch 团队更详细的介绍。

## 2) Lovely Tensors——为人类阅读而生的 Tensor

[Lovely tensors](https://github.com/xl0/lovely-tensors/) 是一个旨在帮助调试 PyTorch 神经网络代码的库。

随着网络变得越来越大、越来越复杂，跟踪代码中的所有张量和变量会变得很有挑战。[Lovely tensors](https://github.com/xl0/lovely-tensors/) 库提供了一组工具和特性，让调试更轻松、更高效。我最近才发现这个库，虽然还没在自己的工作中大量使用，但它看起来非常有趣且实用。

[![lovely-tensors](https://sebastianraschka.com/images/blog/2023/open-source-highlights-2022/lovely-tensors.webp)](https://github.com/xl0/lovely-tensors/)

## 3) Jupyter Notebook 中的多 GPU 训练支持

作为一个经常用 Jupyter notebook 做原型和教学的人，我一直在寻找改进工作流的方法。

Jupyter notebook 的一个局限是，由于多进程限制，它们不支持深度学习中许多现代的多 GPU 范式。这就是为什么我对最近发布的 PyTorch Lightning 1.7 感到兴奋——它在 Jupyter notebook 中为 PyTorch 引入了多 GPU 支持。

[![multi-gpu](https://sebastianraschka.com/images/blog/2023/open-source-highlights-2022/multi-gpu.webp)](https://lightning.ai/pages/community/tutorial/multi-gpu-jupyter-notebooks/)

对所有同时使用 PyTorch 和 Jupyter notebook 的人来说，这是一个非常方便的特性。你可以在[这里](https://lightning.ai/pages/community/tutorial/multi-gpu-jupyter-notebooks/)进一步了解这个新特性。

## 4) Scikit-learn 1.2：打磨一款基础机器学习库

我最喜欢的机器学习库之一 scikit-learn 的最新版本于 12 月发布。对我来说，一些亮点更新包括对 `HistGradientBoostingClassifier`（LightGBM 的一个实现）的增强。`HistGradientBoostingClassifier` 新支持的特性包括：

1. 交互约束（在树中，沿特定路径出现的特征被视为"交互"）；
2. 类别权重；
3. 类别特征的名称。

另一个亮点是新的 `.set_output()` 方法，我们可以配置它返回 DataFrame 对象：

例如

```python
scalar = StandardScaler().set_output(transform="pandas")
scalar.fit(X_df)

# X_trans_df is a pandas DataFrame
X_trans_df = scalar.transform(X_df)
```

或者

```python
log_reg = make_pipeline(
    SimpleImputer(), StandardScaler(), LogisticRegression())
log_reg.set_output(transform="pandas")
```

这将帮助我们在未来省去许多需要到处传递列名的变通做法。

完整变更列表可以在[发布说明](https://scikit-learn.org/1.2/whats_new/v1.2.html#changes-1-2)中找到。

## 5) Embetter：面向 Scikit-Learn 的嵌入

最近，机器学习领域出现了一股使用预训练大语言模型和视觉 Transformer 的潮流。过去我讨论过[训练和使用 Transformer 的各种方式](https://twitter.com/rasbt/status/1585001572719030272?s=20&t=vOriOyNhUEg4tHFV8jRYtw)。一种特别便利的做法是：用预训练模型生成嵌入（embedding），然后把这些嵌入喂给下游的其他模型。

我最近偶然发现了 [embetter](https://github.com/koaning/embetter)，一个围绕计算机视觉和文本嵌入的小型 scikit-learn 兼容库。用 `embetter`，你可以用 4 行代码构建一个分类器流水线，在 Transformer 的句子嵌入上训练逻辑回归模型：

```python
text_emb_pipeline = make_pipeline(
  ColumnGrabber("text"),
  SentenceEncoder('all-MiniLM-L6-v2')
  LogisticRegression()
)
```

它大概不会刷新什么预测性能纪录，但在处理文本和图像数据集时，它是一个不错的快速性能基线。

## 6) 以 Lightning 般的速度训练、部署和发布 AI 产品

你们中的一些人可能知道，我在今年早些时候加入了一家初创公司（Grid.ai）。夏天，Grid.ai 更名为 [Lightning AI](https://lightning.ai)，我们发布了开源的 Lightning AI 框架。

我们的平台让用户能够构建 AI 产品、训练和微调模型，并把它们部署到云端，而不必操心基础设施、成本管理、扩展等技术难题。

[![lightning](https://sebastianraschka.com/images/blog/2023/open-source-highlights-2022/lightning.webp)](https://lightning.ai)

下面我会分享两个动手构建 AI 产品的例子，但如果你偏好自底向上的方式，我写了两篇博客文章来解释 `lightning` 库的工作原理：

- [用 Lightning 分享深度学习研究模型 第一部分：构建超分辨率应用](https://sebastianraschka.com/blog/2022/lightning-app-srgan-1.html)
- [用 Lightning 分享深度学习研究模型 第二部分：利用云端](https://sebastianraschka.com/blog/2022/lightning-app-srgan-2.html)

## 7) Muse：把扩散模型投入生产

我们 Lightning AI 团队发布了 [Muse 应用](https://lightning.ai/muse)，展示如何使用 Lightning AI 框架（上文提到的）把 Stable Diffusion 这样的大模型投入生产。该项目的开源代码在 GitHub 的[这里](https://github.com/Lightning-AI/stable-diffusion-deploy)。

[![Open source highlights 2022 muse](https://sebastianraschka.com/images/blog/2023/open-source-highlights-2022/muse.webp)](https://lightning.ai/muse)

该应用附有一篇循序渐进的文章（[Diffusion Models in Production](https://lightning.ai/pages/community/tutorial/deploy-diffusion-models/)），介绍了经验教训和注意事项——如果你想让模型扩展到数千用户，从自动扩缩容到动态批处理都需要考虑。

## 8) 用 Whisper 生成高质量字幕

OpenAI 最近发布并开源了 [Whisper](https://github.com/openai/whisper)，一个用于为音频文件生成字幕（closed captions）和摘要的开源语言模型。我拿 Whisper 试跑了一下，效果惊人地好。与 YouTube 默认的字幕生成方式以及我这些年试过的几家付费服务相比，Whisper 生成的字幕准确度高得多。尤其令我印象深刻的是，它对我的口音和深度学习技术行话的处理都相当到位。

希望这对你也有用，[这是我用来](https://gist.github.com/rasbt/0d09932c861851f177bd8f13dc93b354)为[我在 YouTube 上的深度学习课程视频](https://sebastianraschka.com/blog/2021/dl-course.html)重新生成字幕的脚本。

[![echo](https://sebastianraschka.com/images/blog/2023/open-source-highlights-2022/echo.webp)](https://lightning.ai/echo/)

顺便打个广告：我们最近发布了 [Echo 应用](https://lightning.ai/echo/)，它为 Whisper 提供了一个友好的界面，可以直接从电脑拖放视频。

与使用 Stable Diffusion 模型的 Muse 应用类似，Echo 展示了用 Lightning AI 框架把大模型投入生产并扩展到多用户的能力。

当然，Echo 是完全开源的。想了解它是如何构建的，请看 [Deploy OpenAI Whisper as a Cloud Product](https://lightning.ai/pages/community/tutorial/deploy-openai-whisper/) 教程。

## 9) MLxtend 的特征分组更新

我仍在（偶尔）维护 [MLxtend](http://rasbt.github.io/mlxtend/)——这个机器学习工具库是我 2012 年读研究生时启动的。

在今年的一些新增功能中，[MLxtend v0.21](http://rasbt.github.io/mlxtend/CHANGELOG/) 现在支持在特征选择过程中把相关特征（例如由独热编码产生的特征）作为一个整体来处理。这项更新让用户能更轻松地一起处理和分析多个相关特征。

[![Open source highlights 2022 feature groups](https://sebastianraschka.com/images/blog/2023/open-source-highlights-2022/feature_groups.webp)](http://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/)

## 10) (Bio)Pandas 中的 AlphaFold 蛋白质结构

我仍在维护的另一个小库是 [BioPandas](https://biopandas.github.io/biopandas/)。

BioPandas 是一个让计算生物学家以熟悉的 pandas DataFrame 格式处理蛋白质结构文件的库。例如，Protein Data Bank（PDB）格式应用广泛，但可以更方便一些。BioPandas 的目标是让用户能够借助功能强大且友好的 pandas 库来操作这些文件，从而在现代编程语言中更轻松地处理它们。

[![biopandas](https://sebastianraschka.com/images/blog/2023/open-source-highlights-2022/biopandas.webp)](https://biopandas.github.io/biopandas/tutorials/Working_with_mmCIF_Structures_in_DataFrames/)

现在 `PandasPdb` 和 `PandasmmCIF` 两个类都支持获取 [AlphaFold 2](https://alphafold.ebi.ac.uk) 结构。例如：

```python
protein = PandasPdb().fetch_pdb(uniprot_id='Q5VSL9', source="alphafold2-v2")

protein = PandasMmcif().fetch_mmcif(uniprot_id='Q5VSL9', source='alphafold2-v2')
```

## 结语

开源比以往任何时候都更具吸引力、更加活跃。例如，过去一年里，[超过四分之三的组织增加了对开源软件的使用](https://www.zdnet.com/article/open-source-is-more-important-than-ever-say-developers-heres-why/)。

上面列出的只是一小部分浮现在我脑海中的开源项目，绝算不上全面。（如果你还意犹未尽，我推荐我的 Tryolabs 朋友们每年发布的 [Top Python libraries you should know about](https://tryolabs.com/blog/2022/12/26/top-python-libraries-2022) 榜单。）
