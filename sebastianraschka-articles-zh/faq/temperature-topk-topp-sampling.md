---
title: "温度、top-k 与 top-p 采样"
title_en: "Temperature, top-k, and top-p sampling"
source: https://sebastianraschka.com/faq/docs/temperature-topk-topp-sampling.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 温度、top-k 与 top-p 采样

温度（temperature）、top-k 和 top-p 控制着下一 token 采样的不同环节。温度改变所有 token 的相对概率。top-k 把采样限制在固定数量的候选中。top-p 则把采样限制在概率累加达到所选阈值所需的自适应数量候选中。

这些操作发生在模型产生下一 token 的 logit 之后。它们改变的是如何从这些得分中选出一个 token。模型的权重和学到的知识保持不变。

![GPT 模型在其词表上产生下一 token 概率。解码将这个分布转换为被选中的一个 token。](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/proba-index.webp)

## 温度对 logit 做重新缩放

假设模型给 token \(i\) 赋予 logit \(z\_i\)。在正温度 \(T\) 下，采样概率为

\[p\_i(T) = \frac{\exp(z\_i / T)}{\sum\_j \exp(z\_j / T)}, \qquad T > 0.\]

温度为 1 时 softmax 分布保持不变。介于 0 和 1 之间的值会使分布变尖锐，给最强的候选分配更多概率。大于 1 的值会使分布变平坦，让较弱的候选获得更多机会。

对于任意正温度，把每个 logit 除以同一个值不会改变它们的排名。最可能的 token 仍然是最可能的 token。改变的是各 token 之间的概率比值。

`temperature = 0` 需要一点说明。零在公式中是未定义的，因为它会导致除以零。许多生成 API 把零解释为贪心解码（greedy decoding）请求，即不采样、直接选择最大的 logit。这是一种实现惯例，而不是温度缩放。当 \(T\) 从上方趋近于零时，分布趋近于 argmax 分布。

## Top-k 保留固定数量的候选

Top-k 保留得分最大的 \(k\) 个 token，把其余所有 token 从候选中剔除，并在采样前对保留下的概率重新归一化。

![Top-k 采样保留得分最高的候选，对其概率重新归一化，然后采样一个 token。](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/topk.webp)

当 `top_k = 1` 时，只剩下 logit 最大的 token，因此选出的 token 与贪心解码相同。当该值至少等于词表大小时，不会产生任何过滤效果。

这个固定大小并不对所有分布都同样合适。当某个 token 占主导时，保留 50 个候选可能放进一长串弱选项。当分布较平坦时，只保留 5 个又可能删掉若干合理的续写。

## Top-p 保留自适应的概率质量

Top-p，即**核采样（nucleus sampling）**，首先把 token 按概率从高到低排序，然后保留累积概率达到或超过 \(p\) 的最小前缀。被保留的概率在采样一个 token 之前会重新归一化。

因此候选数量在每个生成步骤都可能变化。一个尖峰分布可能两个 token 就达到 `top_p = 0.9`。一个较平坦的分布可能需要几十甚至几百个。设置 `top_p = 1` 通常会禁用该过滤。

核采样由 Holtzman 及其同事在 [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) 中提出。其自适应截断的设计意图是排除不可靠的尾部，同时不把一个固定的候选数量强加给每个分布。

三个控制项可以总结如下。

| 控制项 | 改变什么 | 候选集合 |
| --- | --- | --- |
| 温度 | 相对概率比值 | 除非应用其他过滤器，所有 token 都保持可选 |
| Top-k | 排名截断 | 在其他掩码之后至多 \(k\) 个 token |
| Top-p | 累积概率截断 | 随每一步的分布而变化 |

## 一个简单的概率示例

假设五个 token 的下一 token 概率为

\[[0.50,\ 0.25,\ 0.15,\ 0.07,\ 0.03].\]

取 `top_k = 3` 时，最后两个候选被移除。前三个概率之和为 0.90，重新归一化后约为

\[[0.556,\ 0.278,\ 0.167].\]

取 `top_p = 0.80` 时，前两个 token 不够，因为它们的累积概率只有 0.75。纳入第三个后达到 0.90，所以在这一步 top-p 保留了同样的三个 token。如果排头 token 的概率是 0.88，同样的 top-p 设置就可能只保留那一个 token。

温度会在计算这种截断之前修改概率。对原始分布施加 \(T=0.5\) 等价于把各概率平方后重新归一化。结果约为

\[[0.734,\ 0.183,\ 0.066,\ 0.014,\ 0.003].\]

排名没有变化，但第一个 token 现在获得了多得多的概率质量。

## 各设置如何相互作用

常见的解码顺序是：先用温度重新缩放 logit，然后应用 top-k 或 top-p 过滤，再对保留的得分重新归一化，最后采样一个 token。不同库的确切顺序可能不同，尤其是在同时启用重复惩罚和两种截断方法时。

在 top-p 之前应用温度很重要，因为温度会改变累积概率，从而可能改变核的大小。正温度不会改变哪些 token 属于 top-k 集合，因为它们的排名保持不变。当 top-k 与 top-p 一起使用时，最终候选池通常同时受两条规则约束。

![解码选中一个 token 后，自回归生成会把它追加到上下文中并重复该过程。](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/proba-to-text.webp)

调试时，贪心解码是一个有用的基线，因为它消除了采样随机性。对于开放式生成，适中的温度搭配 top-p 或 top-k 可以允许多个合理续写同时排除弱选项。最佳取值取决于检查点和任务，因此我会从模型官方发布的生成配置入手，而不是在所有模型上复用同一组设置。

它们的直接作用对象是输出多样性。它们无法增加事实性知识或推理能力。更高的温度可以展现更多备选结果，但也可能增加错误。更窄的候选集可以让输出更稳定，但也可能加剧重复。关于[重复循环](https://sebastianraschka.com/faq/docs/repetition-loops-generation.html)的相关 FAQ 讲解了该失败模式，而[自回归生成概览](https://sebastianraschka.com/faq/docs/autoregressive-text-generation.html)展示了解码在完整 token 循环中的位置。
