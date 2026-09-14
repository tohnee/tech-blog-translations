---
title: "为什么模型训练损失很低，生成的文本却依然很差？"
title_en: "Why can a model have low training loss but still generate poor text?"
source: https://sebastianraschka.com/faq/docs/low-loss-but-poor-text.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么模型训练损失很低，生成的文本却依然很差？

训练损失低只说明在当前所用的损失计算方式下，模型对训练目标的预测很好。而生成文本质量差仍可能来自过拟合、训练或生成管线中的 bug、不合适的解码设置，或者下一个 token 似然与我们希望完整回答所具备的行为之间的错位。

我会按上述顺序排查这些可能性，而不是把损失和生成样本看成相互矛盾的证据。

**首先，检查低的是哪个损失。** 训练损失可以持续下降，而验证损失却停滞不前或开始上升。这就是大家熟悉的过拟合情形。模型更紧密地记住了训练序列，却在没见过的文本上没有改善。因此，从目标使用场景中划分出的保留验证集，比最终的训练损失更有参考价值。

验证计算应使用与训练相同的分词器和下一个 token 目标。模型还应处于评估（evaluation）模式，以便关闭 dropout。在 PyTorch 中，`torch.no_grad()` 可以在这类计算中节省内存，但它不能替代 `model.eval()`。

![训练与验证曲线有助于区分「在训练集上持续改善」与「泛化到未见文本」](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/train-steps.webp)

**其次，核实损失衡量的确实是目标任务。** 对于 token 序列 `[t0, t1, t2, t3]`，输入应是 `[t0, t1, t2]`，目标应是 `[t1, t2, t3]`。如果目标不小心等于输入，残差路径会让「重建当前 token」变得远比「预测下一个 token」容易。缺少[因果掩码](https://sebastianraschka.com/faq/docs/causal-attention.html)也会让每个位置读到未来的 token，通过目标泄漏产生很低的损失。

一个有用的健全性检查（sanity check）是未训练基线。当词表大小为 \(V\) 且预测近似均匀时，期望交叉熵约为 \(\ln(V)\)。对于拥有 50,257 个 token 的 GPT-2 词表，这个值约为 10.8。如果一个随机初始化的模型一开始损失就低得反常，就值得仔细检查目标偏移、掩码、填充（padding）和损失的归约方式。

填充也会扭曲结果。被填充的目标位置通常应当被忽略。我会打印一个批次的输入 token ID、移位后的目标 ID、解码后的字符串以及逐 token 损失来检查。这个小测试比再跑一次训练更快地抓住许多数据管线的错误。其构造方法在[LLM 预训练的输入-目标训练样本是如何构造的？](https://sebastianraschka.com/faq/docs/input-target-pretraining-examples.html)（How are input-target training examples constructed for LLM pretraining?）中有更详细的展示。

**如果训练和验证损失看起来都合理，就去测试生成代码。** 先用贪心解码，让下一个 token 就是最终位置 logits 的 `argmax`。确认代码加载的是预期的检查点、使用与之匹配的分词器、从上下文的最后一个位置选取 logits、把选中的 token ID 追加到上下文，并在正确的文本结束（end-of-text）token 处停止。一个 instruct 模型还需要使用它微调时见过的对话模板（chat template）。

分词器不匹配的破坏性尤其大。同一个整数 ID 在两个不同词表下可能代表不同的文本。在这种情况下，模型在训练时的损失可能完全正常，但换用另一个分词器解码时就会产出乱码。

![自回归生成反复从最终位置的 logits 中选出一个 token 并追加到上下文](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

一旦贪心生成正常了，就可以重新引入采样。温度过高或候选集过宽可能放进许多不太可能的 token；温度过低或 top-k 过窄则可能让输出变得重复。把贪心输出与几组温和的设置做对比，有助于区分是模型问题还是解码问题。各个控制参数的说明见[温度、top-k 和 top-p 采样有什么区别？](https://sebastianraschka.com/faq/docs/temperature-topk-topp-sampling.html)（How do temperature, top-k, and top-p sampling differ?）。

**最后，可能真的存在目标错位。** 交叉熵是对很多位置上的下一个 token 误差取平均。它并不直接为事实准确性、指令遵循或段落级连贯性打分。训练时，每个预测拿到的都是来自数据集的正确前置 token；而生成时，模型以自己先前生成的结果为条件，一个糟糕的选择就可能把后续内容带入它不熟悉的上下文。

这解释了为什么一个模型可以取得不错的验证损失，却产出乏味、重复或无助的文本。数据集质量和模型规模同样重要。一个小模型可以学会狭窄语料中常见的局部模式，却没有发展出产出长而连贯回答所需的能力。为「续写」而训练的基座模型也可能只是「补全」提示词，而不是把提示词当作指令来遵循。

因此，我会把损失当作训练诊断指标，而对生成样本单独评估。固定的提示词、面向任务的检查和人工评审能揭示平均 token 损失无法捕捉的失败模式。损失与困惑度的相关区别见[困惑度是什么，它到底能告诉我们 LLM 的什么？](https://sebastianraschka.com/faq/docs/perplexity-what-it-means.html)（What is perplexity, and what does it actually tell us about an LLM?）。
