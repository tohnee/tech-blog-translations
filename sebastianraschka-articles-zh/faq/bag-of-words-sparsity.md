---
title: "为什么词袋表示是稀疏的"
title_en: "Why Bag-of-Words Representations Are Sparse"
source: https://sebastianraschka.com/faq/docs/bag-of-words-sparsity.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么词袋表示是稀疏的

> 原文：[Why Bag-of-Words Representations Are Sparse](https://sebastianraschka.com/faq/docs/bag-of-words-sparsity.html) · Sebastian Raschka's FAQ

这取决于你的词表和数据集，但通常而言：是的，绝对是！

根据定义，如果一个矩阵的大部分元素为零，它就被称为「稀疏」矩阵。在词袋（bag-of-words）模型中，每个文档被表示为一个词频计数向量。这些计数可以是二值计数（某词是否出现）或绝对计数（词频，或归一化计数），而该向量的大小等于词表中的词条数量。因此，如果你的大多数特征向量都是稀疏的，那么我们的词袋特征矩阵也很可能是稀疏的！

现在的问题是：「这些特征向量什么时候是稀疏的？」这实际上取决于我们词表的大小，以及训练语料库中文档的长度和多样性。例如，训练集中的文档越短、越相似，我们最终得到稠密矩阵的可能性就越大——尽管在实践中这仍然极不可能发生！

来看一个简单的例子……假设我们有 3 个文档：

- Doc1: Hello, World, the sun is shining
- Doc2: Hello world, the weather is nice
- Doc3: Hello world, the wind is cold

那么，我们的词表会是这个样子（使用 1-gram，不去除停用词）：

Vocabulary: [hello, world, the, wind, weather, sun, is, shining, nice, cold]

对应的二值特征向量为：

- Doc1: [1, 1, 1, 0, 0, 0, 1, 1, 0, 0]
- Doc2: [1, 1, 1, 0, 0, 1, 0, 1, 1, 0]
- Doc3: [1, 1, 1, 1, 0, 0, 1, 0, 0, 1]

我们用它构造出如下稠密矩阵：

[[1, 1, 1, 0, 0, 0, 1, 1, 0, 0]
[1, 1, 1, 0, 0, 1, 0, 1, 1, 0]
[1, 1, 1, 1, 0, 0, 1, 0, 0, 1] ]

可以看到，其中有 17 个 1 和 13 个 0；所以按照定义，这不算一个稀疏矩阵。不过，我们也能由此体会到这种情形在真实应用中有多罕见 ;)
