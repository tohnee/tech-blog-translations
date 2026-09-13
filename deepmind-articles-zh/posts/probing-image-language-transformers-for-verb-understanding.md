---
title: "探测图像-语言 transformer 的动词理解能力"
title_en: "Probing Image-Language Transformers for Verb Understanding"
source: https://deepmind.google/blog/probing-image-language-transformers-for-verb-understanding/
site: deepmind
date: 2022-02-23
crawled: 2026-09-13
translated: 2026-09-13
---

# 探测图像-语言 transformer 的动词理解能力

> 原文：[Probing Image-Language Transformers for Verb Understanding](https://deepmind.google/blog/probing-image-language-transformers-for-verb-understanding/) · Google DeepMind

将语言锚定到视觉上是许多现实世界 AI 系统的基本问题，例如图像检索或为视障人士生成描述。要在这些任务上取得成功，模型必须把语言的不同侧面——如物体和动词——与图像关联起来。例如，要区分下面中间一列的两张图片，模型必须分辨"接住"（catch）和"踢"（kick）这两个动词。动词理解尤其困难，因为它不仅要求识别物体，还要求理解图像中不同物体之间的相互关系。为攻克这一难题，我们推出了 SVO-Probes 数据集，并用它来探测语言与视觉模型的动词理解能力。

![SVO-Probes 数据集的图示，展示主语、动词、宾语变化对应的正例与负例图像。左列："一只动物躺在草地上"（负例：人躺在草地上，正例：刺猬躺在草地上）。中列："一名球员试图接住球"（负例：球员踢足球，正例：球员接住橄榄球）。右列："一名女子在海滩上慢跑"（负例：女子在树林中慢跑，正例：女子在海滩上慢跑）。](https://lh3.googleusercontent.com/RtKffj2shtU7cSglfXUB4SL1eKWNvAwoH-ejLy0Zfyf-_I6JHSsXrX1jUs8OV29lqLXWGaZ6DH4g00GfwyzFurRGUEuMxSROeIgzw75vdT8pdR7tsA=w1440)

具体来说，我们考察多模态 transformer 模型（如 Lu et al., 2019；Chen et al., 2020；Tan and Bansal, 2019；Li et al., 2020），它们在各种语言与视觉任务上表现出色。然而，尽管在基准测试上表现强劲，这些模型是否具备细粒度的多模态理解仍不明确。此前的工作表明，语言与视觉模型可以不靠多模态理解就拿下基准：例如，仅凭语言先验回答关于图像的问题（Agrawal et al., 2018），或在为图像生成说明文字时"幻觉"出图像中不存在的物体（Rohrbach et al., 2018）。为了预判模型的局限，Shekhar et al. 等工作提出了专门的评测方法，以系统性地探测模型的语言理解能力。但此前的探测集在物体和动词的数量上都很有限。我们开发 SVO-Probes，正是为了更好地评估当前模型在动词理解上的潜在局限。

SVO-Probes 包含 48,000 个图像-句子对，测试 400 多个动词的理解。每个句子都可以拆解为一个<主语，动词，宾语>三元组（即 SVO 三元组），并配上正例与负例图像。负例只在一个方面不同：主语、动词或宾语被替换。上面的图展示了主语（左）、动词（中）或宾语（右）与图像不匹配的负例。这种任务构造让我们能够分离出模型最难处理的是句子的哪些部分。它也使 SVO-Probes 比标准图像检索任务更具挑战性——在后者的负例中，图像往往与查询句子完全无关。

为了构建 SVO-Probes，我们用一个常见训练数据集 Conceptual Captions（Sharma et al. 2018）中的 SVO 三元组去[查询图片搜索](https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list)。由于图片搜索的结果可能带有噪声，我们增加了一个初步标注步骤来过滤检索到的图像，确保得到干净的图像-SVO 对。由于 transformer 是在图像-句子对而非图像-SVO 对上训练的，我们需要图像-句子对来探测模型。为收集描述每张图像的句子，标注者为每张图像撰写一个包含该 SVO 三元组的短句。例如，给定 SVO 三元组<animal, lie, grass>，标注者可以写出"An animal lays in the grass."这个句子。然后我们利用 SVO 标注为每个句子配上一张负例图像，并在最后的标注环节请标注者核验这些负例。详见下图。

![流程图，概述 SVO-Probes 的数据收集管线：将预训练数据中的句子解析为主语、动词、宾语（SVO）三元组，通过搜索 API 检索图像，再经由人工标注进行核验，并与标注者撰写的句子及负例图像配对。](https://lh3.googleusercontent.com/2M8Jy9yOIoPRk7pP60N55NR5HNi7FM_UbzxHQj_uq5DAvr9MGb1in7HMk0dtcvQeRLIavPjen1Ovt6PhoMnu9hRLI1Feso0eQVfyL81cSRG0mCHJwA=w1440)

我们考察多模态 transformer 能否准确地将样本分类为正例或负例。下面的柱状图展示了我们的结果。我们的数据集颇具挑战性：我们的标准多模态 transformer 模型总体准确率为 64.3%（随机水平为 50%）。在主语和宾语上准确率分别为 67.0% 和 73.4%，而在动词上性能降至 60.8%。这一结果表明，动词识别对视觉与语言模型而言确实充满挑战。

![柱状图，展示 SVO-Probes 的分类准确率结果。纵轴为 45% 到 80% 的准确率，50% 处的虚线代表随机水平。图中四根柱子分别是：动词（Verb，蓝色）60.8%，主语（Subject，橙色）67.0%，宾语（Object，绿色）73.4%，总体（Overall，红色）64.3%。](https://lh3.googleusercontent.com/mN7-7Bjdfm_YOsWh3zZaPDQKvWknqzP5dXNDexFM7dbz7f_HnYX4pMr_F4htMmYH3hgIz5VUnCB5ULwpiJIK-sYAMZYu6gUO7JEUbrV61VWCxl9K=w1440)

我们还探索了哪些模型架构在我们的数据集上表现最好。出人意料的是，图像建模能力较弱的模型反而优于标准 transformer 模型。一个假设是，我们的标准模型（图像建模能力更强）对训练集过拟合了。由于这两个模型在其他语言与视觉任务上表现都较差，我们的针对性探测任务揭示了其他基准上观察不到的模型弱点。

总体而言，我们发现尽管多模态 transformer 在基准测试上表现出色，它们仍在细粒度理解上表现挣扎，尤其是细粒度的动词理解。我们希望 SVO-Probes 能帮助推动语言与视觉模型中动词理解的探索，并启发更多有针对性的探测数据集。

欢迎在 GitHub 上访问我们的 SVO-Probes [基准](https://github.com/deepmind/multimodal_transformers)与[模型](https://github.com/deepmind/svo_probes)：基准与模型。
