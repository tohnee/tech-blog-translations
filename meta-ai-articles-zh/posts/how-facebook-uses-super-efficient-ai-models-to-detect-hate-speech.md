---
title: "Facebook 如何用超高效 AI 模型检测仇恨言论"
title_en: "How Facebook uses super-efficient AI models to detect hate speech"
date: 2020-11-19
source: http://ai.facebook.com/blog/how-facebook-uses-super-efficient-ai-models-to-detect-hate-speech
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 如何用超高效 AI 模型检测仇恨言论

> 原文：[How Facebook uses super-efficient AI models to detect hate speech](http://ai.facebook.com/blog/how-facebook-uses-super-efficient-ai-models-to-detect-hate-speech) · Meta AI（Wayback 存档）

2020 年 11 月 19 日

构建能够分析复杂文本的 AI，还不足以保护人们免受有害内容侵害。我们需要这样的系统：发现一条充斥俚语或故意拼错的仇恨言论——并在不到一秒的时间内、以数十亿人的规模完成。这在部署仇恨言论检测系统时一直是个挑战，因为当今最强大、最前沿的语言理解系统使用拥有数亿乃至数十亿参数的大规模 Transformer 模型。包括 Facebook AI 的 RoBERTa 和 XLM-R 在内的新模型一再刷新最先进水平，但这些收益来自不断增大、需要海量计算的模型。

为了释放这些强大 AI 模型的能力，Facebook AI 近期开发了一种名为 Linformer 的新 Transformer 架构，使大规模高效使用它们成为可能。Linformer 是首个在理论上被证明为线性时间的 Transformer 架构。对标准 Transformer 而言，所需算力随输入长度呈几何级增长；而在 Linformer 中，计算量仅以线性速率增长。这使得用更长的文本训练模型、从而获得更好性能成为可能。我们如今正使用 Linformer 分析 Facebook 和 Instagram 在全球不同地区的数十亿条内容。（图表比较了不同 Transformer 架构的复杂度水平。）

连同其他 AI 进展，Linformer 帮助我们在捕获仇恨言论和煽动暴力内容方面取得稳步进展。两年前，我们从平台上移除的仇恨言论中，在被举报之前就被处理的只占很少一部分。而正如 Facebook 今天发布的季度《社群守则执行报告》所详述的，AI 主动检测出了我们移除的仇恨言论的 94.7%。

今年早些时候，我们发表了关于 Linformer 的研究并开放了代码，让其他研究者和工程师可以改进他们的模型。自 2013 年 Facebook AI Research（FAIR，Meta 基础人工智能研究院）实验室成立以来，我们一直坚持开放科学的路线。我们的研究模式围绕发布代码与方法论、与业界和学术界的研究者协作、以及创建开放基准与挑战赛展开。我们在这里分享 Linformer 的工作原理，以及我们如何用它保障平台上人们的安全。这些都是困难的问题，我们的系统仍远非完美。而且即便拥有完美的 AI 工具，关于什么政策最能服务人们，仍然存在艰难的抉择。但 AI 的进步已让我们的平台变得更好、更安全，我们也在努力进一步推进我们的技术。

## 一种构建前沿 AI 模型的更简单方式

Transformer 模型已无处不在：语言建模、机器翻译、语音识别、符号数学、计算机视觉和强化学习。Transformer 依赖于一种简单而强大的机制——自注意力（self-attention），它使 AI 模型能够有选择地关注输入的某些部分，从而更好地理解内容。但它们出了名地消耗资源，因为其自注意力机制会随着输入序列长度的增长，需要越来越多的内存和计算。当你把输入规模从比如 4000 增加到 8000 时，计算量并不是翻倍，而是从大约 1600 万增至 6400 万。

Linformer 通过对注意力矩阵中的信息做近似——而不降低模型性能——克服了这一挑战。如上图所示，即使输入规模增长，Linformer 模型也能高效地做出预测。（示意图展示了 Linformer 如何产出低秩矩阵。）为构建 Linformer，我们首先证明了自注意力可以做低秩近似，这表明有可能在不降低性能的情况下大幅简化标准 Transformer 架构。（流程图展示了如何用 Linformer 创建检测仇恨言论的模型。）

随着序列长度增加，Linformer 的效率收益也随之增长。在典型的 Transformer 中，每一层的每个 token 都必须查看（或关注）上一层的其他每一个 token。这产生了二次方复杂度，因为算法必须对当前层的 n 个 token 中的每一个，遍历上一层的 n 个 token。我们用 RoBERTa Transformer 模型在 WIKI103 和 IMDB 两个大型数据集上计算了特征值（衡量矩阵近似秩的标准度量），从而能够证明：上一层 N 个 token 的信息可以压缩成一个更小的、固定大小的 K 个独立单元的集合。有了这种压缩，系统只需对每个 token 遍历这个更小的 K 单元集合。换言之，自注意力是所谓的低秩（low-rank）的，可以用一个更小的数字矩阵来表达。（谱分析图展示了 Transformer 模型自注意力矩阵的谱。）

## 接下来是什么

这些效率收益之所以重要，是因为我们希望在仇恨言论有机会传播之前就处理它。判断一条帖子是否违反政策时，毫秒都很关键。Linformer 正在帮助我们做到这一点，但它还可能催生当前尚不可能实现的新 AI 完整性系统。有朝一日，我们能否部署一个从文本、图像和语音中学习的最先进模型，不仅有效检测仇恨言论，还能检测人口贩卖、霸凌和其他形式的有害内容？在达成这一目标之前还有很多工作要做，但 Linformer 让我们更近了一步。此外，通过让大规模 Transformer 模型更高效，Linformer 还让较小的研究实验室和工程团队——即使没有大规模计算资源——也能训练和测试最先进的 AI。

我们致力于保障平台上人们的安全。我们相信 Linformer 和其他 AI 进展将使我们继续取得进步，也期待看到其他人在我们工作之上的构建与推进。
