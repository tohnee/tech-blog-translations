---
title: "用深度学习翻译编程语言"
title_en: "Deep learning to translate between programming languages"
date: 2020-07-21
source: http://ai.facebook.com/blog/deep-learning-to-translate-between-programming-languages
crawled: 2026-09-22
translated: 2026-09-22
---

# 用深度学习翻译编程语言

> 原文：[Deep learning to translate between programming languages](http://ai.facebook.com/blog/deep-learning-to-translate-between-programming-languages) · Meta AI（Wayback 存档）

2020 年 7 月 21 日

把一个代码库从 COBOL 这类古老的编程语言迁移到 Java 或 C++ 这样的现代替代方案，是一项困难且耗费资源的任务，需要对源语言和目标语言都有专长。例如，COBOL 至今仍广泛用于世界各地的大型机系统，因此公司、政府和其他机构常常必须选择：要么人工翻译其代码库，要么坚持维护一种可追溯到 20 世纪 50 年代的语言写就的代码。

我们开发并开源了 TransCoder——一个完全自监督的神经转编译器（transcompiler）系统，可以让代码迁移容易得多、高效得多。我们的方法是第一个无需并行数据即可训练、就能把代码从一种编程语言翻译成另一种语言的 AI 系统。我们已经证明 TransCoder 能够成功在 C++、Java 和 Python 3 之间翻译函数。

TransCoder 优于开源和商业的基于规则的翻译程序。在我们的评估中，该模型正确地将超过 90% 的 Java 函数翻译成 C++，74.8% 的 C++ 函数翻译成 Java，68.7% 的函数从 Java 翻译成 Python。相比之下，一款商用工具从 C++ 到 Java 仅能正确翻译 61.0% 的函数，而一款开源翻译器把 Java 函数翻译成 C++ 的准确率仅为 38.3%。

自监督训练对编程语言之间的翻译尤为重要。传统的监督学习方法依赖大规模并行数据集进行训练，但诸如 COBOL 到 C++、C++ 到 Python 的并行数据根本不存在。TransCoder 仅依赖用单一编程语言编写的源代码，而不需要同一段代码在源语言和目标语言中的成对示例。它不需要编程语言方面的专业知识，而且很容易将 TransCoder 的方法泛化到更多编程语言。我们还专门为该领域创建了一个新的评估指标。

TransCoder 可用于把遗留代码库更新为现代编程语言——后者通常更高效、更易维护。它还展示了神经机器翻译技术如何应用于新领域。正如 Facebook AI 此前用神经网络求解高等数学方程的工作一样，我们相信 NMT 可以帮助完成通常不被视为翻译或模式识别的其他任务。

## 专为编程语言构建序列到序列模型

在自然语言领域，神经机器翻译的最新进展已被广泛接受，甚至连专业译者也越来越多地依赖自动机器翻译系统。然而，由于该领域并行数据的稀缺，它们在代码翻译上的应用一直有限。程序员仍然依赖基于规则的代码翻译器（需要专家审查和调试其输出），或者干脆人工翻译代码。

TransCoder 通过将无监督机器翻译的最新进展应用于编程语言，克服了这些挑战。我们构建了一个带注意力的序列到序列（seq2seq）模型，由一个编码器和一个解码器组成，采用 Transformer 架构。TransCoder 使用单一共享模型（部分基于 Facebook AI 此前在 XLM 上的工作）处理所有编程语言。我们按照 Facebook AI 此前研究中详述的无监督机器翻译三原则训练它：初始化、语言建模和反向翻译。

（原文此处附图：该图展示 TransCoder 如何利用无监督机器翻译的三个原则。）

我们首先利用来自开源 GitHub 项目的源代码，用掩码语言模型（MLM）目标预训练模型。与自然语言处理中的情形一样，这种预训练会创建跨语言嵌入：在不同编程语言中用于相似上下文的关键词，在嵌入空间中非常接近（例如 catch 和 except）。这些嵌入的跨语言特性来自各种语言之间大量存在的共同 token（锚点）。锚点的例子包括 C++、Java 和 Python 共有的关键词（例如 for、while、if、try），以及数学运算符、数字和源代码中出现的英文字符串。用 MLM 预训练使 TransCoder 能够生成高质量的输入序列表示。然而，解码器尚不具备翻译能力，因为它从未被训练过基于源表示来解码序列。为解决这一问题，我们用去噪自编码（Denoising Auto-Encoding，DAE）目标训练模型对序列进行编码和解码。DAE 目标的运作类似监督机器翻译算法：模型被训练来在给定一个序列的损坏版本时预测原始 token 序列。作为输入给解码器的第一个符号，是一个指示输出编程语言的特殊 token。测试时，一个 Python 序列可以被模型编码，并使用 C++ 起始符号解码，从而生成 C++ 翻译。C++ 翻译的质量取决于模型的「跨语言性」：如果 Python 函数和一个有效的 C++ 翻译被编码器映射到相同的潜在表示，解码器就能成功生成这个 C++ 翻译。

（原文此处嵌入视频：该图展示功能相似的关键词如何被聚合在一起。）

跨语言模型预训练和去噪自编码本身就足以生成翻译。然而，这些翻译的质量往往较低，因为模型从未被训练去做测试时期望它做的事情，即把函数从一种语言翻译成另一种语言。为解决这一问题，我们使用反向翻译——这是在弱监督场景中利用单语数据最有效的方法之一。我们使用单一模型，每种目标语言使用不同的起始 token。它被并行训练为从源语言到目标语言以及从目标语言到源语言的翻译。目标到源方向的版本用于把目标序列翻译成源语言，生成与真值目标序列对应的带噪源序列。然后可以以弱监督方式训练模型从带噪源序列重建目标序列，并学会从源语言到目标语言的翻译。目标到源和源到目标两个版本并行训练直至收敛。

此前大多数源代码翻译研究评估模型时，依赖自然语言中使用的指标，如 BLEU 分数或其他基于 token 相对重叠的方法。然而这类指标并不适合编程语言。两个句法差异很小的程序可能获得很高的 BLEU 分数，但代码执行结果却大相径庭。反之，语义等价但实现不同的程序会得到很低的 BLEU 分数。另一种指标是参考匹配（reference match），即完美匹配真值参考的翻译所占百分比，但它往往低估翻译质量，因为它无法识别语义等价的代码。为了更好地衡量 TransCoder 和其他代码翻译技术的表现，我们创建了一个名为计算准确率（computational accuracy）的新指标，它评估假设函数在给定相同输入时是否生成与参考相同的输出。我们还在发布我们的测试集以及用于计算该指标的脚本和单元测试。

下面的示例展示 TransCoder 如何将示例代码从 Python 翻译成 C++。我们将以下代码输入模型：

```python
def SumOfKsubArray(arr, n, k):
    Sum = 0
    S = deque()
    G = deque()
    for i in range(k):
        while (len(S) > 0 and arr[S[-1]] >= arr[i]):
            S.pop()
        while (len(G) > 0 and arr[G[-1]] <= arr[i]):
            G.pop()
        G.append(i)
        S.append(i)
    for i in range(k, n):
        Sum += arr[S[0]] + arr[G[0]]
        while (len(S) > 0 and S[0] <= i - k):
            S.popleft()
        while (len(G) > 0 and G[0] <= i - k):
            G.popleft()
        while (len(S) > 0 and arr[S[-1]] >= arr[i]):
            S.pop()
        while (len(G) > 0 and arr[G[-1]] <= arr[i]):
            G.pop()
        G.append(i)
        S.append(i)
    Sum += arr[S[0]] + arr[G[0]]
    return Sum
```

TransCoder 成功地将 Python 输入函数 SumOfKsubArray 翻译成了 C++。它还推断出了参数类型、返回类型和函数的形参。模型把 Python 的 dequeue() 容器对应到了 C++ 实现中的 deque<>。以下是模型输出的 C++ 代码：

```cpp
int SumOfKsubArray(int arr[], int n, int k){
    int Sum = 0;
    deque <int> S;
    deque <int> G;
    for(int i = 0; i < k; i ++){
        while((int) S.size() > 0 && arr[S.back()] >= arr[i])
            S.pop_back();
        while((int) G.size() > 0 && arr[G.back()] <= arr[i])
            G.pop_back();
        G.push_back(i);
        S.push_back(i);
    }
    for(int i = k; i < n; i ++){
        Sum += arr[S.front()] + arr[G.front()];
        while((int) S.size() > 0 && S.front() <= i - k)
            S.pop_front();
        while((int) G.size() > 0 && G.front() <= i - k)
            G.pop_front();
        while((int) S.size() > 0 && arr[S.back()] >= arr[i])
            S.pop_back();
        while((int) G.size() > 0 && arr[G.back()] <= arr[i])
            G.pop_back();
        G.push_back(i);
        S.push_back(i);
    }
    Sum += arr[S.front()] + arr[G.front()];
    return Sum;
}
```

## 推进研究并助力实际应用

自动代码翻译有潜力让公司或开源项目中的程序员更高效，使他们能够更容易地整合公司内其他团队或其他开源项目的各种代码。它还能大幅降低更新用古老语言编写的旧代码库的工作量与成本。转编译技术的进展可以推动公司和其他机构更新到更近期的语言并促进未来的创新，这将使使用其服务的人以及这些机构本身都受益。编程语言机器翻译的进展还可以帮助那些没有时间或无力负担课程来学习多种编程语言的人。

更广泛地说，AI 有潜力协助其他编程任务。例如，Facebook AI 此前发布了 Neural Code Search——一种用自然语言对代码进行查询的方法，以及 Getafix——一个学习自动为代码缺陷建议修复的工具。虽然 TransCoder 并非为帮助调试或改进代码质量而设计，但它有潜力帮助工程师迁移旧代码库，或使用其他语言编写的外部代码。

为了促进未来利用深度学习进行代码翻译的研究，我们还在发布一个测试集，使其他研究者能够用计算准确率（而非对语义不敏感的指标）来评估代码翻译模型。我们期待看到其他人如何在 TransCoder 工作的基础上继续构建，并推进面向新型翻译任务的自监督学习。

**作者**

- Baptiste Roziere，研究助理
- Marie-Anne Lachaux，研究工程师
- Lowik Chanussot，研究工程经理
- Guillaume Lample，研究科学家
