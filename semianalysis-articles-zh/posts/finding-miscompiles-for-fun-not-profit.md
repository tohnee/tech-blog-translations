---
title: "寻找编译器误编译：只为乐趣，不为盈利"
title_en: "Finding Miscompiles for Fun, Not Profit"
subtitle: "或者说：就算没有 Claude Mythos 的访问权限，你也能在一个下午花掉 10,000 美元。"
date: 2026-05-28
source: https://newsletter.semianalysis.com/p/finding-miscompiles-for-fun-not-profit
crawled: 2026-09-15
authors: ["Justin Lebar"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 寻找编译器误编译：只为乐趣，不为盈利

> 原文：[Finding Miscompiles for Fun, Not Profit](https://newsletter.semianalysis.com/p/finding-miscompiles-for-fun-not-profit) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**或者说：就算没有 Claude Mythos 的访问权限，你也能在一个下午花掉 10,000 美元。**

***6 月 1 日更新：**在我们发布本文的次日，Anthropic 发布了 Opus 4.8 以及 Claude Code 中的“ultracode”模式。我们的初步实验表明，两者结合起来在过滤低严重性 bug 方面明显更好，且每发现一个中高严重性 bug 的成本大约只有本文所述工作流的 1/5（误差范围*非常*大）。*

过去十年，我先后在 Google、Waymo 和 OpenAI 从事机器学习编译器方面的工作，包括 clang 的 CUDA 支持、XLA:GPU、Triton 以及 OpenAI 的自研硬件。我见过不少世面。但在过去一周左右的时间里，我经历了职业生涯中最令人不安的事情之一：只用一个下午，我就为了让 AI 智能体跑编译器代码花掉了超过 10,000 美元，在 LLVM 中找到了数百个疑似成立的 bug，其中包括许多误编译（miscompile），至少有一个还**相当严重**。这篇文章讲的就是我如何走到这一步，以及我们可能正走向何方。

![](https://substack-post-media.s3.amazonaws.com/public/images/7bab807d-7d4b-438e-a5e5-ac1166c7f5f6_1672x941.png)

2026 年 1 月，我决定把在 LLVM（clang、rustc 以及 AMD 的 GPU 编译器等背后的编译器）里找 bug 当成一个个人项目。我和 Codex 协作写了一个模糊测试器（fuzzer）。基本思路是：生成一个随机程序，让它经过编译器的一部分处理，然后检查编译后的程序与原程序做的是不是同一件事（通常就是直接把两个程序各跑一遍）。我在它上面花了几周时间，在 LLVM 的[窥孔优化](https://en.wikipedia.org/wiki/Peephole_optimization) pass instcombine 里找到并修复了五个 bug。在那之后，我的 fuzzer 找到新 bug 花的时间越来越长，我也失去了兴趣。

时间快进到 2026 年 5 月中旬。我以承包商身份加入了 SemiAnalysis，并决定尝试把同样的技术用到 NVIDIA 的底层编译器 ptxas 上。我预期这会比 fuzz LLVM 收获更少，原因有几点：

- 一般来说，fuzzer 会“卡住”：一旦发现一个 bug，它们就会不断找到触发同一个 bug 的新路径。对于 LLVM 这样的开源编译器，你“只需”把 bug 修掉，然后继续 fuzz 就行。但对于 ptxas 这样的闭源编译器，你最多只能设法修改自己的 fuzzer，让它不再生成触发同一个 bug 的输入。这种事往好了说也非常繁琐。
- 在 LLVM 上我可以只跑单个 pass（比如 instcombine），而在 ptxas 上我必须端到端跑完整个编译器。我担心这会让某些 bug 需要更大、更复杂的复现用例，从而更难被 fuzzer 发现。
- LLVM 我可以自己构建，因此可以用带插桩的编译选项编译被测程序，帮助 fuzzer 挑选能探索程序新部分的“有趣”输入。虽然 AFL++ 有一些可以从预编译二进制中[收集插桩信息](https://github.com/AFLplusplus/AFLplusplus/blob/3261160/qemu_mode/README.md)的模式，但它们会拖慢被测程序，总体上我并不指望它们能同样有用。（最后 fuzz ptxas 时，我实际上并没有用这些模式，只做了纯无导向的 fuzzing。）

我以为像上次一样，干上几个星期也许能找到一小撮 bug。

结果，三天之内，我就拿到了 40 个被 ptxas 误编译的程序。（一周后，这个数字已经升到约 80 个。）虽然这些测试用例中有一些反映的可能是编译器里同一个底层 bug，我还是相当吃惊。[这些](https://github.com/SemiAnalysisAI/FuzzX/blob/c880b419d7453c2a69d7be6eac517971e17c8eaa/ptx/known-miscompiles/m003-no-lop3-max-chain/reduced.ptx) [复现](https://github.com/SemiAnalysisAI/FuzzX/blob/c880b419d7453c2a69d7be6eac517971e17c8eaa/ptx/known-miscompiles/m001-seed-050f/reduced.ptx) [用例](https://github.com/SemiAnalysisAI/FuzzX/blob/c880b419d7453c2a69d7be6eac517971e17c8eaa/ptx/known-miscompiles/m005-prmt-ifconvert-mask/reduced.ptx) [中有许多](https://github.com/SemiAnalysisAI/FuzzX/blob/c880b419d7453c2a69d7be6eac517971e17c8eaa/ptx/known-miscompiles/m002-structured-lop3/reduced.ptx)可以归约成看起来相当“正常”的指令序列。

如果你想看看我找到的这些 bug（准确说，是 Codex 和 Claude 找到的），它们都在 GitHub 上的 [FuzzX 仓库](https://github.com/SemiAnalysisAI/FuzzX)里。

![](https://substack-post-media.s3.amazonaws.com/public/images/5ebeb550-e2cd-468f-81c5-80c2b333ffdd_1283x928.png)
*来源：GitHub 上的 FuzzX，https://github.com/SemiAnalysisAI/FuzzX/*

为什么这一次我的 fuzzer 写起来容易这么多？据我判断，差别就在 ChatGPT 5.2 和 5.5 之间。这一次，整个 fuzzer 都是我 vibe-code（氛围编程）出来的，我一行代码都没看过。每当我们发现一个 bug，随之修改 fuzzer、免得反反复复卡在同一个 bug 上——这种乏味的活儿全由 LLM 干了。它还会对自己生成的每个测试用例做最小化，常常一干就是一个小时甚至更久。它独立决定 fuzz 哪些 PTX 指令、哪些指令序列是“安全”的（即不会触发未定义行为）。我只是用 `/goal` 把它放进一个循环里，然后就去睡觉了。

先说清楚：fuzzing 能找到 bug 并不令人意外。令人意外的是，我几乎没有付出任何人工，就这么快找到了这么多 bug。

很自然，我的下一个问题是：能不能在 LLVM 的 AMDGPU 后端里也找到 bug？答案是可以，而且速度和我找 ptxas bug 时差不多——这一点你大概不会意外。跑到某个时候，我个人的 ChatGPT Pro 账户额度用光了，我切换到 SemiAnalysis 的 Claude 账户。我没有察觉 Opus 4.7 和 ChatGPT 5.5 之间有任何质量差异，它们都很出色。

故事本来可以到此为止。我把我找到的 bug 报告给了 AMD 和 NVIDIA。截至写作时，AMD 已经修好了其中五个，而且因为他们的编译器是开源的，我可以立刻用上他们的修复。如果其中哪个 bug 对我至关重要，我甚至可以自己动手修。开源工具链万岁。

到这一步，我的 ptxas 和 AMDGPU fuzzer 开始慢了下来：跑得越来越久，却找不到新 bug。我几乎就此打住，但脑子里冒出一个念头：如果我就是让 Claude 通读 LLVM 去找 bug 呢？换句话说，我造 fuzzer，是不是因为我没有真正领会[苦涩的教训](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)（Bitter Lesson）？

我让 Claude 一次派出 50 个子智能体去找 bug。好家伙，bug 源源不断地涌来。Claude 找 bug 的速度达到*每四分钟一个*。（相比之下，这时 fuzzer 找一个新 bug 已经要花好几个小时。）

我的第一反应是：我甚至不觉得这说明 LLVM 的 AMDGPU 后端特别多 bug。事实上，有朋友建议我对 x86 后端如法炮制，结果它产 bug 的速度接近*每分钟两个*。

在我叫停之前，我的找 bug 智能体毫无放缓的迹象。我不知道外面还有多少问题。大概很多？

自动化找 bug 通常要回答的问题是：“这些 bug 要紧吗？”x86 的 bug 我目前只梳理了约 20%。智能体找到的 bug 平均而言确实不如 fuzzer 找到的严重：fuzzer 找到的每一个 bug 都是可确证的误编译，而智能体是在用自己的判断力决定什么算 bug、什么不算，有时候它们会判断错。

另一方面，我检查过的 30 个左右智能体发现的 bug 里，有一个是这个[极其吓人](https://github.com/llvm/llvm-project/pull/199592)的案例：LLVM 会把一个原子（atomic）存储拆成两个非原子存储。这个 bug 很难通过 fuzzing 发现（fuzz 原子操作很难），而一旦发生在生产环境，后果很可能既相当糟糕又非常难查根因（因为把原子存储降级为非原子存储，99% 的时候都没事，只有 1% 的概率会毁掉你的数据）。

你该问的另一个问题是：这一切花了多少钱？vibe-code 出来的 fuzzer 相对便宜。同时编写 AMD 和 NVIDIA 两个 fuzzer 那阵子，我的用量大约是我 $200/月的 ChatGPT Pro 账户每周配额的两倍。换成按 token 计费的 Opus 4.7 就贵多了，几天的活儿大约花了 $1000 的量级。我不知道换成 Claude Max 账户会不会更便宜，也不知道我用 Claude 做的这些活儿是不是比我早先用 Codex 做的更耗 token。

另一方面，让一大军子智能体去读代码，嗯，可一点都不便宜。几个小时之内我花掉了超过 10,000 美元，而且我甚至没开快速模式。（谢谢 Dylan 的 token！）虽然这种方式找到的 bug 平均严重性低于 fuzz 找到的，但代码审查能发现一整类用 fuzzing 极难发现的 bug，仅这一点对我就很有价值。

坦白说，光是上面提到的那个原子操作 bug，在合适（或者说不合适）的条件下造成的损失就可能远超 10,000 美元；这种静默数据损坏几乎能击垮任何生产系统。而且即便你的系统有防护措施、能察觉这类损坏，你多半还是得烧掉几个月的工程时间去追查它的源头。如果重来一次，只要预算够我放出一群智能体，我根本不会费劲去 fuzz。

我仍在试着消化这次经历的意义。我觉得它比一句“只要子智能体够多，所有 bug 都是浅的”要大得多。也许教训是这句：

> **五个月前不可能的事，如今“只是”非常贵而已。**

一个推论是：如果你*没有*这个预算，那你所能触及的可能性空间就比有预算的人更小。而且我预计，这个差距在未来几个月还会大幅拉大。

我跑智能体的那天，SemiAnalysis 花在我的 token 上的钱比付给我的报酬高出一个数量级。如果一样东西的价值取决于别人愿意为它付多少钱，那么这是我职业生涯中第一次，我给雇主创造的价值低于我的 AI。

这让我不禁想：六个月后，SemiAnalysis 会愿意为 token 花多少钱？而那些付不起、或者不愿付的人和公司，日子会是什么样？

最后一个想法。我之所以能对 LLVM 的 AMDGPU 和 x86 后端用“让 Claude 读代码”的办法，是因为我有源代码。ptxas 我手里只有一个二进制，没法这么干。但是……我有多大的把握，认为只要 token 够多，Opus 5.7（甚至 4.7）就无法只靠读汇编就找到 bug？
