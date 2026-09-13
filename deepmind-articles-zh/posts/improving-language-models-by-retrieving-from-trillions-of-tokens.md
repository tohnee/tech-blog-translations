---
title: "从数万亿 token 中检索以改进语言模型"
title_en: "Improving language models by retrieving from trillions of tokens"
source: https://deepmind.google/blog/improving-language-models-by-retrieving-from-trillions-of-tokens/
site: deepmind
date: 2021-12-08
crawled: 2026-09-13
translated: 2026-09-13
---

# 从数万亿 token 中检索以改进语言模型

> 原文：[Improving language models by retrieving from trillions of tokens](https://deepmind.google/blog/improving-language-models-by-retrieving-from-trillions-of-tokens/) · Google DeepMind

近年来，自回归语言建模的显著性能提升，主要来自增加 Transformer 模型的参数量。这导致训练能耗大幅上升，并催生了一代参数量超过 1000 亿的稠密「大语言模型」（LLM）。与此同时，人们还收集了包含数万亿词的大型数据集，以支持这些 LLM 的训练。

我们探索了一条改进语言模型的替代路径：为 transformer 增加一个针对文本段落（包括网页、书籍、新闻和代码）数据库的检索机制。我们把这种方法称为 RETRO，即「Retrieval Enhanced TRansfOrmers」（检索增强 Transformer）。

![Retrieval Enhanced Transformer（RETRO）架构示意图：输入序列查询一个 2 万亿词的检索数据库以找到相邻文本段落，这些相邻段落由 Transformer 编码器处理，再通过与自注意力和前馈层交错排布的交叉注意力层，生成符合事实的输出序列。](https://lh3.googleusercontent.com/lYNi-AqFlA3pfPnWLqSctAtdNiqc7YNypluBwFQf_AnfcIbPHV_JmNMYLMz6dlkAWxZyAJ_u_Z55KkHk5cdkszU079Ut2zCDcU2Ks5M2Q7mMCT-k4bs=w1440)

图 1：Retrieval Enhanced TransfOrmers（RETRO）概览。

在传统的 transformer 语言模型中，模型规模与数据规模的好处是绑定在一起的：只要数据集足够大，语言建模性能就受限于模型的大小。而 RETRO 则不局限于训练期间见过的数据——它可以通过检索机制访问整个训练数据集。与参数量相同的标准 Transformer 相比，这带来了显著的性能提升。我们表明，随着检索数据库规模的增大，语言建模性能会持续改善，至少到 2 万亿 token 为止——相当于 175 个人一生的连续阅读量。

![折线图显示，当检索数据库规模增大至 2 万亿 token 时，评估比特每字节（数值越低越好）持续下降，涵盖 172M、425M、1.5B 和 7.5B 参数四种 RETRO 模型规模。不带检索的基线模型（0 token）在 y 轴上以「x」标记表示。](https://lh3.googleusercontent.com/tukJA8I3-EIxYEk7XHOZe7DfYWwqD7oJS25dmkd0aA5bzosuZw5oVk_OdHs-Lb8XcyU7JINqoU9BxiP4p-9PCF7nWFda0-aq5ELy9doyhUGTcdjC=w1440)

图 2：增大检索数据集的规模可带来模型性能的大幅提升。

对每个文本段落（约相当于文档中的一段话），系统会执行一次最近邻搜索，返回训练数据库中找到的相似序列及其后续内容。这些序列有助于预测输入文本的后续内容。RETRO 架构在文档层面交错使用常规的自注意力，并在更细的段落层面与检索到的相邻内容进行交叉注意力。这使得生成的后续内容既更准确，也更符合事实。此外，RETRO 提升了模型预测的可解释性，并提供了一条通过对检索数据库进行直接干预来改善文本续写安全性的途径。在我们基于标准语言建模基准 Pile 的实验中，一个 75 亿参数的 RETRO 模型在 16 个数据集中的 10 个上超越了 1750 亿参数的 Jurassic-1，并在 16 个数据集中的 9 个上超越了 2800 亿参数的 Gopher。

下面我们展示了 7B 基线模型和 7.5B RETRO 模型的两个样本，凸显了 RETRO 的样本相比基线样本更符合事实、也更切题。

![给定圆周率前 100 位数字作为输入提示时生成文本输出的对比。基线 7.1B 模型样本幻觉出了错误的数字，而 RETRO 7.5B 模型样本成功检索并续写了圆周率精确的数学序列。](https://lh3.googleusercontent.com/oHXq-pFgx9VSfPy9eQbc7Gl8I_1uKGUl70PBwIymgkFQuppSbgQUMGcZZhBHh5BAqu_fkyqxasWctbivHEl3VLmheq_wejlnP7pXeyHAkmZtgi9kVg=w1440)

图 3：基线模型只生成了 2 位正确的数字。而使用 RETRO，正确的数字在数据库检索之后被生成出来。

![一组文本对比，展示模型对输入提示「Beavers are interesting animals that live near rivers. They build」（河狸是有趣的动物，生活在河边。它们建造）的生成结果。基线 7.1B 样本从河狸开始，但很快跑题去谈论青蛙和金毛寻回犬。相比之下，RETRO 7.5B 样本则继续输出仅与河狸筑坝及使用牙齿有关的、符合事实的准确信息。](https://lh3.googleusercontent.com/Hxp8tPIM9Hxp7v-4XlgkFOtXL7zgsQnR6eftJIghYgUPdiZ-ypyHynDPD04xnr75coGR4ulINqTGMe5lHY1R_bUA6uNJSJTVNAbX0eQ_A8RDXUTk8FM=w1440)

图 4：RETRO 模型比基线样本更切题。（可选）在此输入图片说明
