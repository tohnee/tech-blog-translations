---
title: "第 12 讲：LLM 服务——投机解码"
title_en: "LLM Serving: Speculative Decoding"
source: https://cs2680.seas.harvard.edu/slides/12_llm_serving_spec_decoding.pdf
pages: 78
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 12 讲：LLM 服务——投机解码

> PDF 讲义文本抽取：[12_llm_serving_spec_decoding.pdf](https://cs2680.seas.harvard.edu/slides/12_llm_serving_spec_decoding.pdf) · Harvard CS2680

## 第 1 页

**现代 AI 系统：智能体与系统优化**

Juncheng Yang

LLM 服务：投机解码

## 第 2 页

**事务**

- 课程概览
  - 上一次服务课（11 月 4 日）：批处理、分页与并行
  - 今天：投机解码；下一次：KV 缓存，然后是量化
- 事务
  - 作业 5（Mads-Stack）今天发布；11 月 24 日（周二）23:59 截止
  - 11 月 18 日（周三）：展示你的作业 4 服务引擎
  - 11 月 25 日（周三）不上课（感恩节假期）

## 第 3 页

**今日安排**

- 投机解码的基础
- 草稿模型
- 验证
- 系统

## 第 4 页

**基础**

- 为什么解码慢
- 起草、验证、接受
- 拒绝采样与精确性
- 加速比的算术

## 第 5 页

**解码受内存限制**

GPU 内存（HBM）｜内存总线｜计算核｜输出

模型权重 16 GB

Llama-3-8B，FP16

4.8 TB/s

每 token ≥3.3 ms

每加载一字节约 1 FLOP

要喂饱需要约 206

每条序列 1 个 token

“sat”

token 一个一个出来：每一步都要等前一步

Step 1: “The”——重读 16 GB

Step 2: “cat”——重读 16 GB

Step 3: “sat”——重读 16 GB

Step 4: “on”——重读 16 GB

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

问题：权重流入时计算核却闲着。这些算力可以用来做什么？

## 第 6 页

**廉价地起草，并行地验证**

自回归：每次前向 1 个 token

投机：每轮 1 到 k+1 个 token

target pass +1｜target pass +1｜target pass +1｜target pass +1

verify pass +4｜verify pass × +1｜verify pass × +3

时间 →

1. 起草：小模型猜 k 个 token
2. 验证：大模型一次检查全部 k 个
3. 接受：接受正确的猜测，再加一个 token

draft（k = 3）｜accepted｜× rejected｜discarded from target

在同样的时间里，投机解码产出 8 个 token（4 + 1 + 3），而不是 4 个。

Fast Inference from Transformers via Speculative Decoding

Accelerating Large Language Model Decoding with Speculative Sampling

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

问题：草稿模型是更弱的模型。输出怎么还能与目标模型一致？

## 第 7 页

**拒绝采样让廉价的猜测变得精确**

例子：p(x) = 3x²，x ∈ [0, 1]

抽 X、U 均匀分布于 [0, 1]；若 U ≤ X² 则保留 X。

U

x = 0.2 → 保留 4%

x = 0.8 → 保留 64%

保留：U ≤ X²｜重试：U > X²

被保留的 X 密度 ∝ x²。

在 [0, 1] 上 x² 的积分为 ⅓，所以归一化后得到 3x²。

红色占正方形的三分之一：3 个中保留 1 个。

一般规则

选一个你能采样的提议分布 q，以及常数 M，使对所有 x 都有 p(x) ≤ M·q(x)。

抽 X ~ q；以概率 p(X) / (M·q(X)) 保留它，否则重试。

为什么有效

q(x) × p(x)/(M q(x)) = p(x)/M

x 被提议的频率 × 被保留的概率，剩下 p(x)/M，所以保留下来的样本服从 p。M 次抽样中保留 1 次：q 越接近 p，浪费越少。

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 8 页

**拒绝采样可以作用在 token 上**

M = 2 时，蓝色覆盖红色

提议：2 × q｜目标：p

0.6 “cat”：全部保留

1.2 “dog”：4 个中保留 1 个

0.2 “rat”：2 个中保留 1 个

扔掉浅色部分；红色被留下。

1. 提议：草稿模型 q 选一个词。
2. 检查：以红色 ÷ 蓝色的概率保留它：p(x) / (2·q(x))。
3. 重试：如果被扔掉，就再选一次。

同一规则，M = 2：保留下来的词服从 p，平均每个词抽 2 次。

投机解码的版本

它去掉了 ×2：以概率 min(1, p/q) 保留草稿 token。不重试：被拒绝时从 p 采样，所以每一轮都能产出一个 token。

Various Techniques Used in Connection with Random Digits

Fast Inference from Transformers via Speculative Decoding

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 9 页

**每一轮都起草、验证并接受**

1. 起草：小模型 q 逐个猜出 k 个 token x̃1 … x̃k。波浪号表示猜测。
2. 验证：大目标模型 p 一次前向给全部 k 个猜测打分，并多算它们之后的一个位置。
3. 接受：从左到右，以公式 (1) 的概率接受每个 x̃i。遇到第一次拒绝时，从 (2) 重采样并停止。
4. 奖励：如果全部 k 个猜测都存活，就从目标模型最后一次前向中再取一个 token。它是免费的。

(1) 接受一个猜测

以概率 min(1, p(xi)/q(xi)) 接受 xi

p(x) 和 q(x) 分别是两个模型对 token x 的概率。若 p ≥ q，总是接受。

(2) 拒绝后重采样

x ~ p′(x) = max(0, p(x) − q(x)) / Σx′ max(0, p(x′) − q(x′))

从 p 比 q 更想要的那些 token 中抽取，并重新缩放到总和为 1。

Fast Inference from Transformers via Speculative Decoding

Accelerating Large Language Model Decoding with Speculative Sampling

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 10 页

**以概率 min(1, p/q) 接受**

接受概率 = min(1, p(x)/q(x))

如果目标模型至少和草稿模型一样喜欢这个猜测，就总是接受。

例子：词表有三个 token；草稿模型猜了其中一个。

| token | 目标 p | 草稿 q | 接受概率 | 原因 |
| --- | --- | --- | --- | --- |
| “cat” | 0.6 | 0.3 | 1 | q < p：总是接受 |
| “dog” | 0.3 | 0.6 | ½ | q > p：2 个中接受 1 个 |
| “rat” | 0.1 | 0.1 | 1 | q = p：总是接受 |

要点：只有被过度猜测的 token（“dog”）会被拒绝，而且只在 q 超出 p 的幅度上被拒绝。

Fast Inference from Transformers via Speculative Decoding

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 11 页

**被拒绝的 token 从剩余概率中重采样**

p′(x) = max(0, p(x) − q(x)) / Σx′ max(0, p(x′) − q(x′))

一次拒绝之后，只从目标模型比 q 更想要的那些 token 中抽取。仍是 cat / dog / rat 的例子。

1. 剩余：max(0, p − q)
2. 重新缩放到总和为 1
3. 为什么吻合

cat 0.3 / dog 0 / rat 0；剩余总和 = 0.3

cat 1.0 / dog 0 / rat 0

0.3 ÷ 0.3：全部落在 “cat” 上

接受率 α = Σ min(p, q) = 0.3 + 0.3 + 0.1 = 0.7

拒绝发生的频率为 1 − α = 0.3，与剩余总量 0.3 相同。

所以重采样恰好补上剩余部分：给 “cat” +0.3。

要点：重采样恰好补回规则 (1) 拒绝掉的那部分概率。

Fast Inference from Transformers via Speculative Decoding

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 12 页

**接受概率加重采样概率等于 p**

Pr(emit 𝑥) = min(p(x), q(x)) + max(0, p(x) − q(x)) = p(x)

每个 token 经由各条路径被输出的概率

逐 token 核对

cat：0.3 + 0.3 = 0.6 = p ✓

dog：0.3 + 0 = 0.3 = p ✓

rat：0.1 + 0 = 0.1 = p ✓

与目标 p 的总和相同。

所有青色 = α：0.3 + 0.3 + 0.1 = 0.7

要点：对每个 token，两条路径的概率加起来都回到 p，所以输出严格服从 p。

Fast Inference from Transformers via Speculative Decoding

图中：p = 0.6 / p = 0.3 / p = 0.1，对应 cat / dog / rat；猜测被接受｜重采样

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 13 页

**投机解码是精确的**

一个 token x 有两条出路：被猜中并接受，或者被拒绝后重采样为 x。

Pr(emit 𝑥) = min(p(x), q(x)) + max(0, p(x) − q(x)) = p(x)

猜中 x 并被接受｜被拒绝、随后重采样为 x｜目标 p 的概率｜x 被输出的概率

当 q(x) < p(x)：草稿模型过于保守

q(x)　p − q

q(x) 全部被接受；重采样补上 p − q。

当 q(x) > p(x)：草稿模型过于激进

p(x)　q − p

只有 p(x) 被接受；多出的 q − p 被拒绝。

Fast Inference from Transformers via Speculative Decoding

Accelerating Large Language Model Decoding with Speculative Sampling

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

问题：输出是精确的。但检查 k 个额外 token 要花多少成本？

## 第 14 页

**验证成本很低**

3.3 ms｜拐点｜16.6 ms

0 / 5 / 10 / 15 / 20

1　256　512　768　1024

每次前向的时间（ms），按该次前向的 token 数

Llama-3-8B FP16，一块 H200，理想 roofline：T(n) ≈ max(W / B, n·W / F)

n：每次前向的 token 数｜B：带宽，4.8 TB/s

W：权重，16 GB｜F：算力，989 TFLOPS

k：每请求的草稿数｜batch：每次前向的请求数

拐点在 n = F / B ≈ 206

每个权重每 token 花 2 字节和 2 FLOPs，所以 n 个 token 花 n·W FLOPs。

批和 k 共享预算

n = batch × (k + 1) ≤ 206 时仍然免费：批 32 时 k ≤ 5，批 64 时 k ≤ 2，从 128 起没有余量。

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 15 页

**接受率决定加速比**

α：草稿 token 被接受的概率

k：每轮的草稿长度

c：草稿步成本 ÷ 目标步成本

每个目标前向的期望 token 数

E = 1 + α + … + αᵏ = (1 − αᵏ⁺¹) / (1 − α)

相对普通解码的加速比

S = E / (ck + 1)

例子：α = 0.8，k = 4，c = 0.05，得到 E ≈ 3.4，S ≈ 2.8×

每个目标前向的期望 token 数：按草稿长度 k 与三种接受率 α 绘制

6.1　α = 0.9

4.3　α = 0.8

2.5　α = 0.6

0 / 1 / 2 / 3 / 4 / 5 / 6 / 7

1 2 3 4 5 6 7 8

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 16 页

**继续加长草稿的收益递减**

当 k → ∞：αᵏ⁺¹ → 0，所以 E → 1 / (1 − α)。

但是：每个草稿步仍然要花 c，所以 S = E / (ck + 1) 先达到峰值，然后趋向 0。

每个目标前向的期望 token 数 E：按草稿长度 k 与三种接受率 α 绘制

相对普通解码的加速比 S：按草稿长度 k 绘制，草稿成本 c = 0.05

α = 0.9

α = 0.8

α = 0.6

0 / 2.5 / 5 / 7.5 / 10

1 5 10 15 20 25 30

4.7×

α = 0.9｜α = 0.8｜α = 0.6

0× / 1× / 2× / 3× / 4× / 5× / 6×

1 5 10 15 20 25 30

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 17 页

**α 衡量 p 与 q 的重叠程度**

𝛼 = Σₓ min(p(x), q(x))

每个 token 只按两个概率中较小的那个计入：α 是两个模型共享的概率质量。

例子：仍是 cat / dog / rat 词表。

| token | 目标 p | 草稿 q | 共享：min(p, q) |
| --- | --- | --- | --- |
| “cat” | 0.6 | 0.3 | 0.3 |
| “dog” | 0.3 | 0.6 | 0.3 |
| “rat” | 0.1 | 0.1 | 0.1 |

α = 0.3 + 0.3 + 0.1 = 0.7

贪心解码

在温度 0 下，每个模型把所有概率都压在一个 token 上，所以 α 就是草稿模型 top token 与目标模型一致的比例。

Fast Inference from Transformers via Speculative Decoding

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 18 页

**更小的草稿模型带来更大的加速**

3.4×｜2.8×｜1.7×

T5-small（77M）｜T5-base（250M）｜T5-large（800M）

相对 T5-XXL（11B）解码的加速比，按草稿模型

英德翻译，贪心解码

为什么更大的草稿模型反而输了

α 几乎不变：0.75、0.80、0.82。

草稿成本增长 10×：从 77M 到 800M 参数，所以 c·k 吃掉了收益。

要点：一个 α 尚可的廉价草稿模型，胜过一个准确但缓慢的草稿模型。

Fast Inference from Transformers via Speculative Decoding

Accelerating Large Language Model Decoding with Speculative Sampling

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 19 页

**更高温度会降低加速比**

3.4×｜2.6×（small）｜2.8×｜2.4×（base）｜1.7×｜1.4×（large）

贪心（T = 0）｜采样（T = 1）

相对 T5-XXL（11B）解码的加速比，按草稿模型

英德翻译；α 从 0.75→0.62、0.80→0.68、0.82→0.71

Fast Inference from Transformers via Speculative Decoding

T = 0 只检查一个 token

当且仅当草稿是 argmax p 时才接受，所以 α 是 top-1 匹配率。

T = 1 检查整个分布形状

分布上的任何不匹配都会降低接受率。

最佳 k 也缩小

在 T = 1 时，最佳 k 从 7 降到 5。

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 20 页

**三个杠杆提升加速比**

𝑆 = 𝐸 / (𝑐𝑘 + 1)

E：每个目标前向的 token 数，由 α 和 k 决定

c·k：k 个草稿步的成本，以目标步为单位

1：验证前向，假定成本为一次解码步

提高 E

与 p 更匹配的草稿模型会提高 α。Token 树尝试在每个位置给出多个猜测。放松的检查会接受近似正确的猜测。

缩小 c·k

复用目标模型的隐藏状态、复制已经见过的文本，或者一次前向起草全部 k 个 token。

让那个 1 保持为 1

只有在计算空闲时，检查 k + 1 个 token 才只花一次解码步。大批次和 MoE 模型会打破这一点。

Fast Inference from Transformers via Speculative Decoding

为什么解码慢｜起草、验证、接受｜拒绝采样与精确性｜加速比的算术

## 第 21 页

**草稿模型**

## 第 22 页

**大多数草稿模型复用目标模型**

草稿来自｜家族｜例子

独立的模型｜独立的小模型｜T5-small、Llama 3.2 1B

目标模型自己的层或隐藏状态｜自投机｜LayerSkip、SWIFT

预测头｜Medusa

特征级草稿模型｜EAGLE、EAGLE-2、EAGLE-3

原生多 token 预测｜DeepSeek-V3 MTP

并行与块草稿模型｜DFlash、DSpark

已经见过的文本｜复制与检索｜N-gram 查找、SuffixDecoding

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 23 页

**DistillSpec 训练草稿模型去"同意"目标模型**

问题：现成的小模型是为质量训练的，而不是为了与某个特定目标模型一致，所以它们的接受率 α 很低，限制了加速比。

动机：α 衡量草稿模型与目标模型共享多少概率，因此蒸馏到与目标模型匹配的草稿模型会获得更高的 α。

核心思路：在草稿模型自己采样的前缀上（on-policy）从目标模型蒸馏，散度按任务和解码策略选择。

DistillSpec: Improving Speculative Decoding via Knowledge Distillation

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

问题：目标模型能不能自己给自己起草，不需要第二个模型？

## 第 24 页

**LayerSkip 用浅层起草**

问题：投机解码通常需要第二个模型：额外的权重和 KV 缓存、匹配的分词器，而且目标模型一更新就要重新训练草稿模型。

动机：许多 token 并不需要每一层，但正常训练的模型中间层无法通过 LM head 解码，所以提前退出得到的草稿很差。

核心思路：用层 dropout 和提前退出损失训练，让浅层也能预测；用第 1 到 ℓ 层起草，用第 ℓ + 1 到 L 层验证，并复用草稿的 KV 缓存。

LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 25 页

**LayerSkip 只验证被跳过的层**

layer ℓ ⋯ layer 1｜共享 LM head｜draft ×k｜layer L ⋯ layer ℓ + 1｜verify

LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding

SWIFT: On-the-Fly Self-Speculative Decoding for LLM Inference Acceleration

成本 ≈ k·ℓ/L + (1 − ℓ/L) 次前向，而独立草稿模型是 k·c + 1

洞见

一个模型、一份缓存：没有草稿权重或第二份 KV 缓存；验证复用第 1..ℓ 层的 KV。

训练让提前退出可用：随深度递增的层 dropout，加上共享 LM head 上的退出损失。

免训练：SWIFT 改为跳过中间层，由贝叶斯优化选择。

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 26 页

**Medusa 增加预测头，向前猜测**

问题：独立的草稿模型难以获得也难以服务：它必须共享分词器、跟踪目标模型的分布，并作为第二个模型与目标模型并行运行。

动机：最后一个隐藏状态已经携带了关于下一个之后 token 的信号，而在它上面加小头的训练成本很低，即使冻结主干也可以。

核心思路：在最后一个隐藏状态上加 K 个头；第 k 个头预测 token t + k + 1。把每个头的 top 猜测组合成一棵树，用树注意力一次前向验证。

Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 27 页

**Medusa 的预测头随深度增加而损失准确率**

一次目标前向：每个头读取同一个 h

h

LM head：sat（t + 1）

head 1：on（t + 2）

head 2：down、the、a（t + 3）

head 3：mat、rug（t + 4）

由各头 top 猜测构成的候选树

洞见

盲猜：每个头读取同一个 h，所以 head 3 看不到 head 1–2 的选择；准确率随深度下降。

树挽回一些准确率：每个头取 top 猜测，剪枝到最常被接受的节点，一次前向验证。

两种训练模式：冻结主干（Medusa-1）或联合微调（Medusa-2）。

Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads

树节点：sat / on / down / the / a / mat

保留：在校准数据上最常被接受的路径

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

问题：后面的头看不到前面的猜测。如果每个猜测都能看到呢？

## 第 28 页

**EAGLE 从目标模型的特征起草**

问题：token 级草稿模型能接受的 token 很少：小模型预测下一个 token 很弱，而 Medusa 的各头彼此看不到对方的猜测。

动机：倒数第二层的特征比 token 更有规律，因此外推效果更好；但采样之后，如果草稿模型不知道被选中的 token，下一个特征就是有歧义的。

核心思路：预测目标模型的下一个特征，而不是下一个 token；把采样得到的 token 喂给草稿模型，让它知道文本往哪个方向走了。

EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty

EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees

EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 29 页

**每个 EAGLE 版本都补上一个缺口**

Li et al.: EAGLE (ICML 2024), EAGLE-2 (EMNLP 2024), EAGLE-3 (NeurIPS 2025); EAGLE-4 Team (2026)

EAGLE-1（ICML 2024）

缺口：小的草稿模型猜 token 猜得很差。

修复：起草特征，并把采样得到的 token 反馈回去。

EAGLE-2（EMNLP 2024）

缺口：对所有上下文用一棵固定树。

修复：按草稿模型的置信度生长树。

EAGLE-3（NeurIPS 2025）

缺口：训练时从未见过自己的猜测。

修复：在自己的输出上训练；融合三层。

EAGLE-4（预印本 2026）

缺口：所有负载用同一个树大小。

修复：根据实测成本确定每棵树的规模。

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 30 页

**EAGLE-1 草稿模型：一层，吃自己的猜测**

EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty

来自目标模型的上下文｜Draft step 1｜Draft step 2

Hidden state → LM head → Next token

h(How) → LM head → can

h(can) → LM head → I

h(I) → LM head → do

h(do) → LM head → it

Drafter（1 层）

Drafter（1 层）

目标模型的隐藏状态｜目标模型采样的 token｜草稿模型的猜测

配对：每个输入把一个隐藏状态与由它产生的 token 配对。

起草：一个解码层预测下一个隐藏状态；目标模型冻结的 LM head 把它变成 token。

重复：第一次猜测之后，草稿模型反馈自己预测的隐藏状态。

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 31 页

**EAGLE-2 生长出置信度塑形的树**

EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees

节点值 = 路径上草稿模型置信度的乘积

depth 1｜depth 2｜depth 3

I

am .70

will .20

going .42

not .14

be .16

go .02

to .38

home .02

there .08

fine .05

最后被接受的 token

已验证：按值取前 6

已起草但被剪枝：“not”（.14）胜过 “there”（.08）

洞见

置信度 ≈ 接受率：草稿模型是校准过的。

先扩展再重排：在每个深度扩展 top-k 节点，然后验证 V 最高的 m 个节点（这里 k = 2、m = 6；论文使用 k = 10、m = 48–60）。

同一个草稿模型：无需重训；比 EAGLE-1 快 20–40%。

上下文决定形状：同样的预算，在可预测文本上用得深，在草稿模型不确定处用得宽。

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 32 页

**EAGLE-3 融合低层、中层和高层**

EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

草稿模型读取目标模型的三层

High layer

Mid layer

Low layer

Target model

EAGLE-1 只读最后一层

融合：concat，然后 FC

融合后的 g，每 token 一个

g 取代最后一层的 h，作为草稿模型的输入。

EAGLE-3 改变了什么

预测 token，而不是特征：特征损失被去掉。

融合三层：低、中、高特征比顶层携带更多信息。

按推理方式训练：后续步骤从草稿模型自己的输出中学习。

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 33 页

**EAGLE-3 在自己的起草输出上训练**

EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

训练时草稿模型的输入序列

EAGLE-1

损失：匹配 h + token｜h(How) can h(can) I h(I) do h(do) it

EAGLE-3

损失：只匹配 token｜g(How) can g(can) I a(I) do a(do) it

目标模型的特征（真实）｜token｜草稿模型自己的输出

EAGLE-1：只在真实隐藏状态上训练，所以后续起草步骤从未在自己的猜测上练习过。

EAGLE-3：从第三个位置起，它读取自己的输出 a(·)，与推理时看到的完全一致。

只用 token 损失：没有隐藏状态需要匹配，草稿模型可以自由地读取融合后的 g。

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 34 页

**EAGLE-4 根据实测成本确定每棵树的规模**

EAGLE-4 Team, 2026, EAGLE-4: One Flexible Drafter for All Batch Sizes and Hardware

同一个草稿模型，树按负载定尺寸

批 1：又宽又深｜大批：短链

草稿模型用更便宜的 LM head

hidden → low-rank head：shortlist → full head on shortlist

草稿成本下降 40% 以上，保留完整词表

普通解码｜投机｜GPU 空闲

洞见

校准一次：按批、上下文和树大小测量验证延迟。

按收益 ÷ 成本生长：只要比值高于阈值就加宽或加深。

一个草稿模型适配所有负载：批 1 或长上下文用深树；大批用链。

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 35 页

**LM head 比草稿模型本身还大**

EAGLE-4 Team, 2026, EAGLE-4: One Flexible Drafter for All Batch Sizes and Hardware

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

每起草步读取的权重

Llama-3-8B 目标模型：隐藏 4,096 × 词表 128,256

两段式 head

隐藏状态：4,096 个数

低秩 head：34M 权重

Shortlist：前几百个

Full-head 行：约 1M 权重

洞见：草稿模型跳过完整的 128K 宽乘积，但任何 token 仍能进入 shortlist。

34M｜220M｜525M

低秩 head｜草稿层｜完整 LM head

## 第 36 页

**EAGLE 在生产中被广泛使用**

EAGLE 在冻结目标模型的特征上训练一个小草稿模型，因此服务商可以为已经在服务的模型加装一个。

Meta：Llama 3 和 Llama 4

EAGLE 用在 Meta 的服务栈中，配合在线蒸馏、树注意力和 H100 上的批处理修复。

大批下快 1.4–2.0×

Baseten：自定义 EAGLE-3 头

为客户模型训练 EAGLE-3 头。生产中快 1.5–2.5×

Efficient Speculative Decoding for Llama at Scale: Challenges and Solutions

How to train custom EAGLE-3 heads for speculative decoding

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 37 页

**DeepSeek-V3 训练自己的草稿模型**

问题：事后训练的草稿模型必须追逐目标模型的分布，而且每次新模型版本都意味着要再训练并服务一个独立草稿模型。

动机：预测更远的未来会加密训练信号，可能有助于规划；联合训练的模块在设计上就与主模型保持一致。

核心思路：一个顺序 MTP 模块（共享嵌入和输出头，一个 Transformer 块）在预训练期间预测 token t+2；推理时它作为 k = 1 的草稿模型。

DeepSeek-V3 Technical Report

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 38 页

**只起草一个 token 让 MTP 的上限接近 2×**

主模型，61 层 → 输出头 → tᵢ₊₁

hᵢ

norm、concat、project → embed tᵢ₊₁

1 个 Transformer 块 → 输出头 → tᵢ₊₂

深红：与主模型共享

蓝色：新的 MTP 权重，一层深

Insights into DeepSeek-V3: Scaling Challenges and Reflections on Hardware for AI Architectures

DeepSeek-V3 Technical Report

洞见

保持因果链：该模块看到真实的 t+1 嵌入，不像 Medusa 的盲头。

接近其上限：k = 1 时 E = 1 + α ≈ 1.9（85–90% 接受率）；实测 1.8× tokens/s。

与模型一起训练：L = Lmain + λ·LMTP（λ = 0.3，之后 0.1）；671B 旁边多了 14B 权重。

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

问题：草稿模型能否一次前向提出一整块 token？

## 第 39 页

**DFlash 一次前向起草一个块**

问题：像 EAGLE 这样的自回归草稿模型要花 k 次顺序前向来起草 k 个 token，因此草稿延迟随 k 增长，限制了往前猜的收益。

动机：扩散语言模型并行填充许多位置，但单独使用时质量下降；作为草稿模型时，它们的错误会被验证抓住，所以只有速度重要。

核心思路：一个轻量块扩散草稿模型，以融合自多个目标层的隐藏特征为条件，在一次前向中预测一个 16 token 的掩码块。

DFlash: Block Diffusion for Flash Speculative Decoding

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 40 页

**在 DFlash 中长块是划算的**

一轮，k = 4 个草稿（示意）

EAGLE 风格：d1 d2 d3 d4 → verify

DFlash：d1–4 → verify（省掉）

一次前向去噪一个掩码块

input：t ▢ ▢ ▢ ▢

light diffusion drafter｜target h

output：t d1 d2 d3 d4

洞见

平坦的草稿成本：所有掩码位置一起填充，所以 16 token 的块只花一次草稿前向。

上下文来自目标模型：草稿层注意融合自多个目标层的隐藏状态。

按使用方式训练：随机锚点，每个锚点之后的块被掩码并并行预测。

DFlash: Block Diffusion for Flash Speculative Decoding

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 41 页

**DSpark 只验证可能的前缀**

问题：并行草稿模型沿块逐渐损失准确率，所以验证整块会浪费其他请求需要的目标模型算力。

动机：额外验证的 token 是否划算，取决于每个请求的接受率和当前负载，因此一个固定的验证长度对多数请求都是错的。

核心思路：在 DFlash 的并行主干上加一个轻量顺序头、一个预测前缀存活率的置信度头，以及一个根据负载设定每个请求验证长度的调度器。

DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 42 页

**在生产中，块草稿模型胜过 MTP**

块草稿模型一次前向填满一整块；在生产中，问题是在负载下每块有多少值得验证。

DeepSeek：DSpark in V4

与 DeepSeek-V4 Flash 和 Pro 同机部署；置信度头在实时流量下设定每个请求的验证长度。

每用户比 MTP-1 快 60–85%

DFlash：SGLang、vLLM、TensorRT-LLM

三个引擎都支持；在 vLLM 上，只需改配置，DFlash checkpoint 就能替代 EAGLE-3。

Gemma 4 31B 上最高 5.8×

DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation

Boost Inference Performance up to 15x on NVIDIA Blackwell Using DFlash Speculative Decoding

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

问题：智能体经常重复已经见过的文本。我们能否不用模型来起草？

## 第 43 页

**基于检索的起草不需要模型**

问题：智能体工作负载会产生长而重复的输出；模型草稿模型忽略了这种重复，而 n-gram 查找只搜索当前提示。

动机：智能体会跨调用重复文本（代码编辑、SQL、工具调用），因此缓存之前的提示和输出，就能以几乎零成本预测长延续。

核心思路：在 CPU 上为过去的输出（全局）和当前请求维护后缀树；匹配最后 p 个 token，并起草一棵最多 α·p 个 token 的树，按每个延续出现的频率打分。

SuffixDecoding: Extreme Speculative Decoding for Emerging AI Applications

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 44 页

**长猜测几乎免费**

过去的输出，保存在 CPU 上的后缀树中

“fix the bug in parser”（×2）、“fix the bug in lexer”、“fix the test”

新请求以 “fix the” 结尾：匹配 p = 2

fix the

bug 3

test 1

in 3

parser 2

lexer 1

蓝色：已起草，是计数最高的路径，最多 α·p = 3 个 token（α = 1.5）

洞见

起草免费：一次 CPU 树查找，而不是一次 GPU 前向，所以 c ≈ 0，长猜测也变得可负担。

按证据投机：匹配越长，草稿越长（α·p）；没有匹配就正常解码。

历史完成了大部分工作：过去请求上的全局树贡献了大部分收益。

依赖工作负载：智能体任务上最高 5.3×，比 EAGLE-2/3 快 2.8×；开放聊天可搭配 EAGLE-3。

SuffixDecoding: Extreme Speculative Decoding for Emerging AI Applications

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 45 页

**在生产中，基于检索的投机解码很常见**

一次编辑会保留文件的大部分内容，所以原文件就是草稿：一次前向验证一长段，只有被改动的区间才逐 token 解码。

Cursor：投机编辑

一个 70B 模型重写整个文件；当前文件提供草稿，因此不运行草稿模型。

快 13×，约 1000 tokens/s

OpenAI：Predicted Outputs

API 调用方把预期输出（通常是当前文件）作为预测发送；匹配的文本会更快返回。

被拒绝的 token 仍然计费

洞见：收益随文件中存活内容的比例扩展；完全重写只能接受少量草稿，会退回普通解码。

Editing Files at 1000 Tokens per Second

Predicted Outputs

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 46 页

**大多数草稿模型复用目标模型**

草稿来自｜家族｜例子

独立的模型｜独立的小模型｜T5-small、Llama 3.2 1B

目标模型自己的层或隐藏状态｜自投机｜LayerSkip、SWIFT

预测头｜Medusa

特征级草稿模型｜EAGLE、EAGLE-2、EAGLE-3

原生多 token 预测｜DeepSeek-V3 MTP

并行与块草稿模型｜DFlash、DSpark

已经见过的文本｜复制与检索｜N-gram 查找、SuffixDecoding

小模型｜自投机｜预测头｜特征级｜原生 MTP｜并行与块｜检索

## 第 47 页

**验证**

## 第 48 页

**SpecInfer 一次前向验证一棵树**

问题：来自单个小模型的单条草稿序列往往很早就出错，而第一次拒绝会扔掉它之后的所有猜测。

动机：在小批下，验证前向会让算力空闲，所以检查许多候选延续与检查一个的成本差不多。

核心思路：把小模型的猜测合并成一棵 token 树，用树掩码一次前向验证每个节点；多步投机采样保持输出精确。

SpecInfer: Accelerating Large Language Model Serving with Tree-based Speculative Inference and Verification

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 49 页

**树能带来更长的被接受序列**

链：每个位置一个猜测

The cat is × on the sat → +1 个 token

树：每个位置 top-2 猜测

The cat → sat / is × → on / down × → on / the mat

+4 个 token，来自 6 个被验证的节点

accepted｜× rejected｜discarded from target

洞见

只要任一子节点通过，整层就通过：一次未命中不再结束整轮。

同一次前向，更多 token：批 1 下，6 个树节点与 3 个链式草稿（第 15 页）花同样的 3.3 ms 前向。

任意形状，一次前向：节点被展平并加掩码，只能看到自己的祖先（下一页）。

SpecInfer: Accelerating Large Language Model Serving with Tree-based Speculative Inference and Verification

问题：每个分支都有自己的历史。一次前向如何检查全部？

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 50 页

**一次前向检查每个分支**

The cat

1 sat

2 is

3 on

4 down

5 on

6 the

1. 展平：追加所有节点；位置 = n + depth。
2. 掩码：每个节点看到上下文和自己的祖先。
3. 打分：一次目标前向给出每个节点的 p。
4. 走路径：保留最长的通过路径，例如 1 → 3 → 6。

注意力掩码：行能看到列

ctx｜1｜2｜3｜4｜5｜6

1 sat

2 is

3 on

4 down

5 on

6 the

兄弟节点永远看不到彼此。

SpecInfer: Accelerating Large Language Model Serving with Tree-based Speculative Inference and Verification

5. 压缩：把该路径的 KV 复制到槽位 n+1..n+3。

位置：n + 1｜n + 2｜n + 3

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 51 页

**不规则批：所有请求一次平坦前向**

Inside vLLM: Anatomy of a High-Throughput LLM Inference System

本步的请求

A：k = 4 → t d1 d2 d3 d4

B：k = 2 → t d1 d2

C：k = 0 → t（关闭投机）

展平

一个验证批：9 个 token

A：t d1 d2 d3 d4

B：t d1 d2

C：t

偏移：0　5　8　9

请求 i 增加 1 + kᵢ 个查询 token；varlen 注意力按每请求偏移索引它们，偏移每一步重建。

一次目标前向

9 个 token 只读一次权重

按偏移拆分

A 得到 5 个输出，B 3 个，C 1 个

按请求采样

接受或拒绝每个请求自己的草稿

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 52 页

**投机要花额外计算**

2.6×｜2.2×｜1.8×｜1.5×｜1.2×

α = 0.5　0.6　0.7　0.8　0.9

每个被保留 token 的目标 FLOPs，相对普通解码

每次前向 k = 4 个草稿；不含草稿 FLOPs｜每保留 token 的成本 = (k + 1) / E

E = (1 − αᵏ⁺¹)/(1 − α)，每前向保留的 token 数

Fast Inference from Transformers via Speculative Decoding

浪费在哪里

α = 0.8、k = 4 时：5 个被验证位置中保留 3.36 个，扔掉 1.64 个。

草稿 FLOPs 还要另加：每轮 k·Nd/Nt 个目标前向；1B→8B、k = 4 时为 0.6。

洞见：在计算受限时，对任何 α < 1，吞吐按 E/(k+1) < 1 缩放，所以那里最佳 k 是 0：k 必须跟随负载，不能固定。

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 53 页

**Sequoia 选择最佳树形状**

问题：固定树形状在树变大后不再增益，top-k 采样在某些温度下失效，而且没有一种树大小适合所有 GPU。

动机：每个子位置的接受率可以针对每对模型测量一次，因此在节点预算下找最佳树是一个优化问题。

核心思路：用动态规划构建使期望接受 token 数最大的树；无放回采样让验证更稳健；剖析器按 GPU 选择树大小和深度。

Sequoia: Scalable, Robust, and Hardware-aware Speculative Decoding

固定树会平台化

top-k

Top-k 会漏掉样本

GPU A｜GPU B

没有一种大小适合所有 GPU

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 54 页

**按 GPU 决定树的规模**

𝐸 ≈ Σ_{v∈T} Π_{u∈path(v)} 𝑐ᵤ　c：草稿模型置信度

The cat

sat .60

is .30

on .48

down .09

on .21

the .43

蓝色 = 保留的 top 4：

E ≈ .60 + .48 + .43 + .30 = 1.81 每前向

Sequoia: Scalable, Robust, and Hardware-aware Speculative Decoding

EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees

Speculative Decoding, SGLang Documentation

洞见

贪心可行：路径值只会缩小，所以 top m 个节点构成一棵树；DP 找到的 token 最多多 33%。

对数收益：接受的 token 随规模大致对数增长，但超过拐点后验证成本线性增长。

在 SGLang 中：`num-steps` = 深度，`eagle-topk` = 宽度，`num-draft-tokens` = m。

问题：精确检查会拒绝正确但不同的 token。我们能否接受它们？

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 55 页

**有损投机解码：放松循环**

Drafter：the old cat sat｜Target 给草稿打分｜Keep?

exact test｜Output

Judge

learned model

1. 起草什么
2. 什么算匹配
3. 谁来验证
4. 测试本身
5. 加一个裁判

精确投机解码起草 token，并用完整目标模型验证它们。每个编号点都是多接受一些草稿的一种方式，而每一种都会改变输出分布。

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 56 页

**起草整个推理步骤**

Drafter：so x = 4｜Target 给该步骤打分｜Keep?

score high?｜Output

Judge

learned model

1. 起草什么
2. 什么算匹配
3. 谁来验证
4. 测试本身
5. 加一个裁判

思路：草稿模型写出整个推理步骤。目标模型或裁判给它打分，只有低分步骤才重新生成。

方法：SpecReason、Lookahead Reasoning、ConfSpec、SPEC-RL

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 57 页

**接受近义 token**

Drafter：the old cat sat｜Target 更偏好 kitten｜Keep?

close enough?｜Output

Judge

learned model

1. 起草什么
2. 什么算匹配
3. 谁来验证
4. 测试本身
5. 加一个裁判

思路：保留与目标模型选择接近的草稿 token，例如目标模型更偏好 “kitten” 时保留 “cat”，或者相邻的图像 token。

方法：LANTERN、grouped SD、speech SSD、Spec-VLA

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 58 页

**用更便宜的目标模型验证**

Drafter：the old cat sat｜Target 的廉价副本｜Keep?

exact test｜Output

Judge

learned model

1. 起草什么
2. 什么算匹配
3. 谁来验证
4. 测试本身
5. 加一个裁判

思路：用目标模型的廉价副本检查草稿，例如稀疏 KV 缓存或更少的激活专家。验证更便宜，但输出会偏离完整模型。

方法：Dustin、MoE-Spec

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 59 页

**放宽接受测试**

Drafter：the old cat sat｜Target 给草稿打分｜Keep?

looser test｜Output

Judge

learned model

1. 起草什么
2. 什么算匹配
3. 谁来验证
4. 测试本身
5. 加一个裁判

思路：用更宽松的规则替代精确接受规则：只要目标模型认为某个草稿 token 足够可能，即使精确测试会拒绝它，也保留。

方法：Lenience、top-β、typical acceptance

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 60 页

**让裁判保留合理的拒绝**

Drafter：the old cat sat｜Target 给草稿打分｜Keep?

exact test｜Output

Judge

can overrule

1. 起草什么
2. 什么算匹配
3. 谁来验证
4. 测试本身
5. 加一个裁判

思路：一个小分类器读取目标模型在被拒绝 token 处的隐藏状态，当这种不匹配不会伤害答案时保留该 token。

方法：Judge Decoding、AutoJudge、SelfJudge、FLy

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 61 页

**有损投机解码的放松点：五个可以多接受的地方**

1. 起草什么：起草整个推理步骤，由奖励模型或裁判打分
   SpecReason、Lookahead Reasoning、ConfSpec、SPEC-RL
2. 什么算匹配：接受与目标模型选择接近的近义 token
   LANTERN、grouped SD、speech SSD、Spec-VLA
3. 谁来验证：用更便宜的目标模型验证：稀疏 KV 或更少专家
   Dustin、MoE-Spec
4. 测试本身：放宽接受规则本身
   Lenience、top-β、typical acceptance
5. 加一个裁判：小分类器推翻部分拒绝
   Judge Decoding、AutoJudge、SelfJudge、FLy

SpecInfer｜树注意力｜精确树验证｜Sequoia｜有损投机解码｜Judge Decoding

## 第 62 页

**在系统中优化投机解码**

## 第 63 页

**投机解码落在一个引擎步之内**

Inside vLLM: Anatomy of a High-Throughput LLM Inference System

起草、验证、接受三阶段的投机解码 token 语义一致

一个请求，k = 4：已提交的最后一个 token t｜draft｜accepted｜rejected

1. Draft

drafter q：The cat sat on the mat

2. Verify

target p：The cat sat on the mat

3. Accept

sampler：The cat sat ✓ on ✓ the ✗ mat ✗

4. Commit

scheduler：The cat sat on a

## 第 64 页

**步时间：GPU 忙起来之前，草稿不花时间**

NVIDIA, 2024: H200 Tensor Core GPU datasheet (4.8 TB/s HBM3e, 989 TFLOPS dense BF16)

每次验证前向的步时间（ms），按批大小

理想 H200 roofline，Llama-3-8B FP16，仅权重

在约 206 token 之前平坦：每次前向都在等 16 GB 权重读取，所以 80 个 token 与 16 个 token 花一样多。

超过之后，每个 token 都增加时间：约每个 0.016 ms，所以 1,280 个 token 要 20.8 ms。

3.3 ms｜5.2 ms｜20.8 ms

k = 4｜4.2 ms

k = 0

0 / 5 / 10 / 15 / 20 / 25

batch 1｜batch 16｜batch 64｜batch 256

320 个 token：越过拐点

## 第 65 页

**大批次抹掉了免费算力**

一次验证前向中每读一份权重对应的 token 数，k = 4

H200 需要约 206 才能保持忙碌（第 5 页）；仅权重

上限 ≈ 206

batch 1：5 个 token

batch 16：80 个 token

batch 64：320 个 token

低于上限时，5 个 token 的成本与 1 个差不多；超过之后，每个 token 都增加时间。

Optimizing Speculative Decoding for Serving Large Language Models Using Goodput

每用户速度 vs 总速度

批 16：k = 4 让每个用户从 299 提升到 1,005 tok/s，步时间仍是 3.3 ms。

批 64：每前向 320 个 token，5.2 ms：每用户 647 tok/s，总计 41K。

批 256：k = 4 把步时间拉长到 20.8 ms：每用户 162 tok/s、总计 41K，低于 k = 0 的 241 和 62K。

理想 H200 roofline，α = 0.8，仅权重，草稿免费。

洞见：批处理和投机消耗同一批约 206 个免费槽位：批处理买到总吞吐，投机买到每用户速度。如何分配是一个 SLO 选择。

批大小｜长上下文｜MoE｜运行时 k

## 第 66 页

**TurboSpec 每一步都选 k**

问题：在连续批处理下，投机可能提高延迟：在高请求率或低接受率时，验证被拒绝的草稿会占用其他请求的算力。

动机：最佳 k 取决于批大小和接受率，而它们每一步都在变；但接受长度和批步时间都是可预测的。

核心思路：有效吞吐 = 生成的 token ÷ 步时间。用每个请求的接受历史预测其接受长度，用线性模型预测步时间；为每个 k 选择使有效吞吐最大的值。

Optimizing Speculative Decoding for Serving Large Language Models Using Goodput

批大小｜长上下文｜MoE｜运行时 k

## 第 67 页

**TurboSpec 每一步运行一个有效吞吐回路**

Optimizing Speculative Decoding for Serving Large Language Models Using Goodput

1. 跟踪 α：接受率的移动平均 α
2. 预测 E：对每个 k（包括 k = 0）预测期望保留 token 数 E(k)
3. 预测 T：用批 token 数的线性模型预测步时间 T
4. 选 k：选 E / T 最高的 k，然后运行该步

下一步：用实际接受的结果更新 α

它的选择（α = 0.8）：batch ≤ 16：k ≈ 5｜batch 64：k ≈ 2｜batch 256：k = 0

批大小｜长上下文｜MoE｜运行时 k

## 第 68 页

**批越大，最佳 k 越小**

2.08×（batch ≤ 16）｜1.86×（batch 64）｜1.00×｜0.42×（batch 256）

0.0× / 0.5× / 1.0× / 1.5× / 2.0× / 2.5×

0 1 2 3 4 5 6 7 8

相对普通解码的有效吞吐，按每步草稿数 k

模型：理想 H200 roofline，Llama-3-8B，1B 草稿模型，α = 0.8

洞见

优化有效吞吐，而不是接受率：Σ Eᵢ(kᵢ) ÷ 步时间；E 来自接受历史，步时间来自线性模型。

最佳 k 随负载缩小：在这个模型中，批 16 及以下约 5，批 64 为 2，256 时为 0；SmartSpec 在小批下看到 > 4。

起草有成本：每个额外草稿增加一次草稿前向（这里 1B 模型为 0.52 ms），所以即使小批也会达到峰值。

永不比关闭更差：峰值负载下不提任何草稿；轻负载下延迟最多降至约 1/3。

Optimizing Speculative Decoding for Serving Large Language Models Using Goodput

问题：大批次抹掉了收益。有什么办法能让投机回来？

批大小｜长上下文｜MoE｜运行时 k

## 第 69 页

**长上下文让投机复活**

问题：人们认为投机只在小批大小下才划算。

动机：在长上下文下，KV 读取占主导，所以大批次仍然受内存限制。

核心思路：在固定大小的稀疏 KV 缓存上起草；在完整缓存上验证。

MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context Generation with Speculative Decoding

目标模型验证完整 KV 缓存

草稿模型在稀疏 KV 缓存上起草

sink（被草稿模型跳过）｜最近窗口

批大小｜长上下文｜MoE｜运行时 k

## 第 70 页

**KV 读取是每个请求私有的**

MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context Generation with Speculative Decoding

权重：一次读取服务整个批

Weights 16 GB

req 1 · 5 tokens｜req 2 · 5 tokens｜…｜req 32 · 5 tokens

每字节 160 FLOPs

32 个请求 × 5 个 token 共享一次权重读取，所以批处理把它推向 H200 保持忙碌所需的 206。

KV 缓存：每个请求读自己的

KV 1 GB，req 1 · 5 tokens｜KV 1 GB，req 2 · 5 tokens｜…｜KV 1 GB … req 32 · 5 tokens

每字节 20 FLOPs

在 8K 上下文下，每个 1 GB 只服务自己的 5 个 token（GQA 下每字节 4 FLOPs），在任何批大小下都远低于 206。

批大小｜长上下文｜MoE｜运行时 k

## 第 71 页

**长上下文下加速比随批增长**

16｜16｜34

20.4 GB｜50.4 GB

1K 上下文｜8K 上下文

每解码步读取的字节，GB

Llama-3-8B，批 32，一块 H200

灰色：权重 · 红色：KV 缓存

MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context Generation with Speculative Decoding

8K 上下文下每次前向的 KV 读取

verify all 8K tokens｜draft skipped｜sink｜window

草稿成本随上下文保持平坦；草稿模型甚至可以是目标模型

洞见

KV 读取不共享：8K 下批 32 每步读取 34 GB KV，而权重只有 16 GB。

注意力仍受内存限制：GQA 下每个 KV 字节约 4 FLOPs，有 k 个草稿时为 4(k + 1)，远小于 206。

超过约 4K token 后收益随批增长：批 32–256 时最高 2.51×（Llama-3.1-8B）。

问题：对 MoE 模型来说，验证 k 个 token 还便宜吗？

批大小｜长上下文｜MoE｜运行时 k

## 第 72 页

**Cascade 为 MoE 关闭投机**

问题：在 MoE 模型上，每个被验证的 token 都路由到自己的专家，所以验证 k 个草稿会读取多得多的权重；一直开启投机会让请求最多慢 1.5×。

动机：收益因模型和任务而异（Mixtral，k = 3：代码上快 39%，数学上慢 54%），但在请求的短窗口内保持稳定。

核心思路：效用 = token 收益 ÷ 验证成本。对每个请求，先短暂测试几个 k，然后在一个较长阶段运行最佳 k；当效用低于 1 时关闭投机。

Utility-Driven Speculative Decoding for Mixture-of-Experts

批大小｜长上下文｜MoE｜运行时 k

## 第 73 页

**短测试限制 MoE 的性能下降**

一个 Mixtral 层，k = 7：8 个专家，每 token 选 2 个

decode 1 token：E1 E2 E3 E4 E5 E6 E7 E8 → 2 个专家

verify 8 tokens：E1 E2 E3 E4 E5 E6 E7 E8 → ≈7 个专家

N(1 − (1 − k/N)ⁿ) ≈ 8 个中的 7.2 个（3.6×）；实测约 3×，因为相邻 token 共享专家。

一个请求上的 Cascade

test run k = 2 → test off → test

短测试、较长的设定阶段；效用 < 1 时关闭投机

洞见

效用短窗口内稳定：短暂测试能预测下一个更长的阶段。

关闭也要一点成本：草稿模型继续运行以保持其 KV 最新（2–3%）。

专家越细伤害越大：在 DeepSeek-V3 中 8 个 token 读取 7.2× 的路由专家，而 Mixtral（均匀路由）是 3.6×。

结果：最坏情况减速 5%，而不是 1.5×；吞吐比静态 k 高 7–14%。

Utility-Driven Speculative Decoding for Mixture-of-Experts

批大小｜长上下文｜MoE｜运行时 k

## 第 74 页

**在运行时决定 k**

SmartSpec：批大小

E 来自接受历史，T 来自线性步时间模型；峰值负载时选择 k = 0。

延迟最多降至约 1/3

Cascade：MoE

在短阶段测试 k；效用低于 1 时关闭投机，但草稿模型继续运行以保持 KV 最新（2–3%）。

最坏情况：慢 5%

DSpark：生产环境

置信度头估计前缀存活率；调度器根据负载画像设定每个请求的验证长度。

每用户快 60–85%

DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation

Optimizing Speculative Decoding for Serving Large Language Models Using Goodput

Utility-Driven Speculative Decoding for Mixture-of-Experts

有效吞吐 = Σᵢ Eᵢ(kᵢ) / T(Σᵢ (1 + kᵢ))：为每个 kᵢ 选择使该值最大的取值。

E：请求 i 的期望保留 token 数 · T：对应批 token 数的步时间

洞见：三者都最大化同一个有效吞吐，区别只在于如何估计 E：接受历史、短试验，或学习得到的置信度头。

批大小｜长上下文｜MoE｜运行时 k

## 第 75 页

**每个想法都拉动三个杠杆之一**

S = E / (ck + 1)

提高 E：每次前向接受更多 token

训练草稿模型去一致：DistillSpec、EAGLE-3

尝试猜测树：SpecInfer、EAGLE-2、Sequoia

接受近义结果：Judge Decoding

缩小 c·k：让起草更便宜

复用目标模型：LayerSkip、Medusa、EAGLE、MTP

一次前向起草全部 k 个：DFlash、DSpark

复制已经见过的文本：N-gram 查找、SuffixDecoding

让那个 1 保持为 1：让验证只花一步

按负载设定 k：SmartSpec、EAGLE-4

在长上下文下投机：MagicDec

对 MoE 关闭投机：Cascade

只验证可能的前缀：DSpark

## 第 76 页

**下一讲**

- 11 月 16 日（周一）：高效 LLM 服务：KV 缓存优化与模型架构（学生主导）
- 11 月 18 日（周三）：学生分享 III：展示你的服务引擎（作业 4）
- 作业 5（Mads-Stack：优化全栈）今天发布；11 月 24 日（周二）23:59 截止

## 第 77 页

**可选主题**

- 有损投机解码

S = E / (ck + 1)

## 第 78 页

（空白页）
