---
title: "第 9 讲：LLM 服务基础（一）——LLM 简介"
title_en: "LLM Serving Basics I: Introduction to LLM"
source: https://cs2680.seas.harvard.edu/slides/9_llm_serving_basics_1.pdf
pages: 36
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 9 讲：LLM 服务基础（一）——LLM 简介

> PDF 讲义文本抽取：[9_llm_serving_basics_1.pdf](https://cs2680.seas.harvard.edu/slides/9_llm_serving_basics_1.pdf) · Harvard CS2680

## 第 1 页

**现代 AI 系统：智能体与系统优化**

Juncheng Yang

LLM 服务基础（一）：LLM 简介

## 第 2 页

**事务**

- 作业 3 于周二 23:59 截止
- 排行榜提交没有迟交日
- 查看网站，确认需要提交哪些内容
- 项目海报展示选项 2：12 月 2 日下午 1–3 点
  - 只有无法参加 12 月 7 日场次时才报名
  - 报名已于上周日截止；如果希望在 12 月 2 日展示，请尽快给我们发邮件

## 第 3 页

**今日安排**

- LLM 简介
  - 一次 LLM 请求的生命周期
  - Transformer 架构[1]
  - 稠密模型、MoE 与进阶变体
- LLM 服务的 GPU 入门[2]
  - GPU 基础
  - GPU 架构
  - GPU 编程与近期 kernel 进展

[1] 本讲假设采用传统的自注意力 Transformer 架构

[2] 我们不会深入细节；目标是帮助你建立直觉

## 第 4 页

**一次 LLM 请求的生命周期**

从提示词到流式文本的六个阶段。

1. 分词（Tokenize）
2. 调度（Schedule）
3. 预填充（Prefill）
4. 解码（Decode）
5. 反分词（Detokenize）
6. 流式输出（Stream）

每个输出 token 重复一次

预填充 → 首 token 时间（TTFT）：整个提示词在一次前向中完成

解码 → 每秒 token 数：每个输出 token 一次前向

## 第 5 页

**阶段 1：分词**

- 文本被切成 token，而不是单词
- 每个 token 约 3–4 个字符
- token 数量决定成本与内存
- 不同模型的分词器不同

“Serving is hard”

Serv / ing / is / hard

1841　288　374　2653

4 个 token——不是 3 个单词

字节级 BPE：从 256 个字节值出发，反复把最频繁的相邻对合并为新 token。没有未知 token。

## 第 6 页

**阶段 2：调度与批处理**

- 请求各自独立到达；GPU 却需要成批处理
- 调度器决定每一步由谁运行
- 连续批处理：运行途中可加入或离开
- 准入数量受 KV 缓存内存限制

step t：R1、R2、R3、（空闲）

step t+1：R1、（空闲）、R3、R4

step t+2：R1、R5、R3、R4

完成的请求离开，新请求加入——无需等待凑满一批

## 第 7 页

**阶段 3：预填充**

- 整个提示词在一次前向中运行
- 所有提示 token 并行地做注意力
- 计算受限；成本随长度增长
- 生成 KV 缓存，输出第 1 个 token

提示 token：t1 t2 t3 t4 t5 t6

对所有 token 做一次前向

第一个输出 token

计算受限 → 首 token 时间（TTFT）

## 第 8 页

**阶段 4：解码生成 logits；采样选出下一个 token**

阶段 4 · 解码

step 1 KV

step 2 KV

step 3 KV

step 4 KV

每个新 token 做一次前向

缓存每一步增长一个 token

带宽受限，因此要批处理

缓存满 → 抢占或排队

阶段 5 · 采样

Temperature　temperature = 0

0：总是取最高分 token；>1：更多 token 成为可能

Top-k　top_k = 50

从最可能的 k 个 token 中采样；k 固定

Top-p（nucleus）　top_p = 0.9

取累计概率达到 p 的最少 token；随置信度自适应

同一模型、同一提示：这些设置会改变答案以及运行时长

## 第 9 页

**阶段 5：反分词与流式输出**

- token ID 一经产生就变成文本
- 不完整的字符先被缓冲
- 流式输出使其具备交互性
- 提前停止可释放缓存内存

用户看到的内容，逐 token：

t1 The

t2 The model

t3 The model streams

t4 The model streams tokens

停止 token、长度限制或连接断开都会结束流

## 第 10 页

**生命周期：要点**

1. 分词：把文本变成 token ID；词表越大，token 越少，但嵌入表越大。
2. 调度：连续批处理让请求在每一步加入和离开；KV 缓存内存限制准入。
3. 预填充：整个提示词在一次计算受限的前向中运行，生成 KV 缓存和第一个 token。
4. 解码与采样：每个 token 一次内存受限的前向；采样从 logits 中选出每个 token。
5. 反分词与流式输出：把每个 token ID 变成文本，并在产生时发送出去。

## 第 11 页

**一窥模型内部**

## 第 12 页

**符号**

模型形状｜工作负载与内存

| 符号 | 含义 | Llama 3 70B |
| --- | --- | --- |
| d | 模型宽度 | 8,192 |
| L | 层数 | 80 |
| H | 查询头数 | 64 |
| Hkv | 键/值头数 | 8 |
| dk | 头维度，d ÷ H | 128 |
| dff | MLP 隐藏宽度 | 28,672 |
| V | 词表大小 | 128,256 |

| 符号 | 含义 | Llama 3 70B |
| --- | --- | --- |
| n | 序列中的 token 数 | 例如 20,000 |
| B | 并发请求数 | 例如 16 |
| N | 参数量 | 70.6B |
| W | 权重字节数（BF16） | 141 GB |
| KV | 每 token 的 KV 字节数 | 320 KB |

KV = 2 × L × Hkv × dk × 2 B

Kᵀ 是 K 的转置

Meta, The Llama 3 Herd of Models, 2024

## 第 13 页

**LLM 是一摞相同的 Transformer 块**

token IDs　输入：文本以整数 token ID 的形式到达

Embedding　嵌入：每个 ID 变成一个向量（8,192 维）

Transformer block × L　Llama 3 70B 有 L = 80 个块，每块都带 norm + 残差

Self-attention　注意力：在 token 之间混合信息

Feed-forward（FFN）　FFN：单独变换每个 token

LM head　LM head：为每个词表 token 给出一个分数

next-token probabilities　Softmax：分数变成概率

Meta, The Llama 3 Herd of Models, 2024

## 第 14 页

**每个块把注意力和 MLP 加到残差流上，两者都先经过 RMSNorm**

ℎ = 𝑥 + Attn(RMSNorm(𝑥))

𝑦 = ℎ + FFN(RMSNorm(ℎ))

RMSNorm(𝑥) = 𝑥 / √(1/d Σᵢ𝑥ᵢ² + 𝜀) ⊙ 𝑔

RMSNorm：按均方根重新缩放；每个维度有一个可学习增益 g

Pre-norm：归一化每个子层的输入，使深层堆叠也能稳定训练

Residual stream：x 流经全部 80 个块；每个子层只添加一个更新

Zhang & Sennrich, RMSNorm, NeurIPS 2019; Xiong et al., ICML 2020; Meta, Llama 3, 2024

## 第 15 页

**自注意力让每个 token 读取所有更早的 token**

- 每个 token 发出一个 query、一个 key 和一个 value
- query · key 分数决定从每个 token 读取多少
- 因果掩码遮住未来的 token
- n 个 token → n² 个分数：成本随上下文增长

softmax(QKᵀ/√dk)·V

key →（列）｜query ↓（行）：The、cat、sat、on、the

0.1　0.2　0.5　0.2　= 1

masked

Vaswani et al., Attention Is All You Need, NeurIPS 2017

为什么除以 √dk？

q · k 要对 dk 个乘积求和，所以它随 dk 增长；缩放可以防止 softmax 饱和。

## 第 16 页

**每个 token 是 X 的一行；权重矩阵把它变成 Q、K 和 V**

The / cat / sat / on / the

X × WQ = Q（n × d · d × dk → n × dk）

Q = X WQ：每个 token 在寻找什么

K = X WK：每个 token 提供什么

V = X WV：每个 token 传递什么

变量：

n：目前已有的 token 数（提示 + 输出）

d：每个 token 向量的数值个数（8,192）

dk：每个 query 或 key 的数值个数，单头（128）

WQ、WK、WV：可学习权重，每个头为 d × dk

head：一个注意力单元；64 个并行运行

Vaswani et al., Attention Is All You Need, NeurIPS 2017

## 第 17 页

**Q Kᵀ 为每一对 token 打分；softmax 把每一行变成权重**

Q（n × dk）× Kᵀ（dk × n）= S（n × n）

÷ √dk，加 M，softmax → A

A（n × n）× V（n × dv）= O（n × dv）

以某一行为例：A 的第 4 行表示 token 4 从 token 1 到 4 各取多少。该行之和为 1。

变量：

Kᵀ：转置后的 key，使每一列对应一个 token

S：分数，第 i 行第 j 列 = query i · key j

M：掩码，对角线以上为 −∞，遮住未来 token

A：权重，每一行之和为 1

dv：value 向量维度（128）

O：输出，每一行是 V 各行的加权混合

Vaswani et al., Attention Is All You Need, NeurIPS 2017

## 第 18 页

**注意力具有 O(n²) 的计算复杂度**

| 步骤 | 公式 | 形状 |
| --- | --- | --- |
| 输入 | X | n × d |
| 查询 | Q = X WQ | n × dk |
| 分数 | S = QKᵀ/√dk | n × n |
| 权重 | A = softmax(S + M) | n × n |
| 输出 | O = A V | n × dv |

每层 FLOPs：Q Kᵀ：2 n² d　　A V：2 n² d　　合计 ≈ 4 n² d

若存储 S 所需内存：n² × heads × layers × 2 B = 8,192² × 64 × 80 × 2 B ≈ 690 GB

FlashAttention 逐块计算 softmax，从不存储 S

Vaswani et al., NeurIPS 2017; Dao et al., FlashAttention, NeurIPS 2022

## 第 19 页

**多头注意力并行运行 64 个小注意力，并用 WO 把它们混合起来**

headᵢ = softmax(QᵢKᵢᵀ/√dk + M) Vᵢ

MHA(X) = Concat(head₁, …, head_H) WO

Split：Q、K、V 拆成 H = 64 个头，dₖ = 8,192 ÷ 64 = 128

Attend：每个头在自己的 128 维上做带掩码的 softmax 注意力

Mix：WO 把各头混合成一个向量

与单个宽头 FLOPs 相同：64 × 128 = 8,192，所以拆分改变的是学到什么，而不是成本

Vaswani et al., Attention Is All You Need, NeurIPS 2017; Meta, Llama 3, 2024

## 第 20 页

**每个头用自己的 128 维做注意力，因此各头学到不同的模式**

输入｜投影｜注意力（5 个 token）

X（n × 8,192）

head 1：Q₁ K₁ V₁ · 128 → 前一个 token

head 2：Q₂ K₂ V₂ · 128 → 第一个 token

head 3：Q₃ K₃ V₃ · 128 → 附近的 token

head 64：Q₆₄ K₆₄ V₆₄ · 128 → 整个上下文

⋮　另外 60 个头

输出｜混合

head₁（n × 128）、head₂（n × 128）、head₃（n × 128）、head₆₄（n × 128）

Concat（n × 8,192）

× WO（n × 8,192）

## 第 21 页

**共享键/值头可以缩小 KV 缓存**

Multi-head（MHA，多头）：8 个查询头，8 个 KV 头，1× KV 缓存大小

Grouped-query（GQA，分组查询）：8 个查询头，2 个 KV 头，¼× KV 缓存大小

Multi-query（MQA，多查询）：8 个查询头，1 个 KV 头，⅛× KV 缓存大小

每 token 的 KV 缓存 = 2 × L × Hkv × dk × 每个值的字节数

Llama 3 70B：64 个查询头共享 8 个 KV 头，因此其 KV 缓存只有 MHA 的 1/8

= 2 × 80 × 8 × 128 × 2 B = 每 token 320 KB，而 MHA 为 2.5 MB

Ainslie et al., GQA, EMNLP 2023; Shazeer, MQA, 2019

## 第 22 页

**以 Llama 3 70B 为例**

d = 8,192：一个 token 向量的宽度

h = 64，dh = 128：64 个 Q 头 × 128 = 8,192

hkv = 8：共享 8 个 KV 头

dff = 28,672：FFN 隐藏宽度，3.5 × d

L = 80：连续的 Transformer 块

V = 128,256：词表中的 token 数

一个 token = 8,192 个数（维度）

KV 1 … KV 8

8,192 → 28,672 个隐藏单元 → 8,192

1 2 3 4 5 6 7 8 … 80

8,192 → 128,256 个分数，每个词表 token 一个

Meta, The Llama 3 Herd of Models, 2024

## 第 23 页

**Llama 3 70B：参数分布在哪里**

Meta, The Llama 3 Herd of Models, 2024

| 组件 | 公式 | 参数量 |
| --- | --- | --- |
| 注意力 / 层 | 2d · H · dk + 2d · Hkv · dk | 151M |
| FFN / 层 | 3 · d · dff | 705M |
| 所有层 | 80 × 856M | 68.5B |
| 嵌入 + LM head | 2 · V · d | 2.1B |
| 合计 | | 70.6B |

## 第 24 页

**系统直觉：权重、计算和 KV 缓存决定预填充、解码与内存**

| 量 | 公式 | 1 个请求 | 64 个请求 |
| --- | --- | --- | --- |
| 预填充（80K token） | B · (2N·n + 2L·d·n²) ÷ FLOP/s | 9.95 s | 637 s |
| 所需显存 | W + B·n·KV | 167 GB | 1,779 GB |

Meta, The Llama 3 Herd of Models, 2024; NVIDIA, H200 datasheet, 2024

权重：2 B × 参数数 → 141 GB

计算：≈ 2 × 参数数 → 141 GFLOPs/token

KV 缓存：2 × L × Hkv × dk × 2 B → 320 KB/token

Llama 3 70B，BF16，在 2× H200 上：1,978 TFLOP/s，9.6 TB/s，282 GB；n = 80,000 token，B = 请求数

如何支持更长的序列？

## 第 25 页

**MoE 用路由器加一组更小的专家 FFN 替换每个块的 FFN**

Shazeer et al., MoE, ICLR 2017; Jiang et al., Mixtral of Experts, 2024

稠密块：Attention；FFN——一个大 MLP，每个 token 都全部运行

替换 FFN →

MoE 块：Attention；Router 选 top-2；E0 E1 E2 E3 E4 E5 E6 E7；加权求和

8 个更小的 FFN；每个 token 只运行 2 个

## 第 26 页

**稠密 vs MoE：内存随总参数扩展，计算随激活参数扩展**

| 模型 | 专家 | 总数 | 每 token 激活 | 权重（BF16） | GFLOPs / token |
| --- | --- | --- | --- | --- | --- |
| Llama 2 70B | 全部（稠密） | 69B | 69B | 138 GB | 138 |
| Mixtral 8x7B | 8 选 2 | 46.7B | 12.9B | 93 GB | 26 |
| Llama 3.1 405B | 全部（稠密） | 405B | 405B | 810 GB | 810 |
| DeepSeek-V3 | 257 选 9 | 671B | 37B | 1,342 GB | 74 |

相同质量、更少计算：Mixtral 以约 1/5 的 FLOPs 达到 Llama 2 70B 的水平；DeepSeek-V3 以约 1/11 的 FLOPs 与 Llama 3.1 405B 相当，但需要 1.7× 的内存。

GFLOPs ≈ 2 × 激活参数。Jiang et al. 2024; DeepSeek-AI 2024; Touvron et al. 2023; Llama Team 2024

## 第 27 页

**进阶 LLM**

滑动窗口

多潜在注意力（Multi-Latent attention）

线性注意力

状态空间模型

稀疏注意力

循环 Transformer（Looped transformers）

多 token 预测

扩散语言模型

ADVANCED —— 可略读，或自行深入阅读

## 第 28 页

**滑动窗口层给 KV 缓存设上限；少量全局层保留长程召回**

全因果｜滑动窗口，w = 3

last token reads all：最后一个 token 读取全部；KV 随 n 增长

last token reads 3：最后一个 token 读取 3 个；KV 上限为 w 个 token

Gemma 3 层模式：L L L L L G —— 5 个局部层（w = 1,024）配 1 个全局层，循环重复

Mistral 7B：每层都是局部层，w = 4,096

Gemma 2：1 个局部层（w = 4,096）∶1 个全局层交替

服务效果：在 128K 上下文下，Gemma 3 存储的 KV 约为全全局层的 1/6

Gemma Team, Gemma 3 Technical Report, 2025

ADVANCED —— 可略读，或自行深入阅读

## 第 29 页

**MLA 为每个 token 存储一个压缩潜在向量**

token h → 压缩 → 潜在向量 c · 缓存 → 展开为 K、V

存储摘要，重建细节：注意力需要时从 c 重新计算 K 和 V

额外数学运算，更少内存：解码时，上投影被折叠进查询权重和输出权重

服务效果：相比 DeepSeek 67B，DeepSeek-V2 将 KV 缓存削减 93%，生成吞吐提升 5.8×

DeepSeek-AI, DeepSeek-V2, 2024; DeepSeek-AI, DeepSeek-V3, 2024

MHA 为每个头缓存 K 和 V｜MLA 只缓存一个潜在向量 c

t1 → t1、c

t2 → t2、c

t3 → t3、c

蓝色 = K，黄色 = V，图中显示 128 个头中的 8 个；虚线 = 从 c 重建、从不存储

ADVANCED —— 可略读，或自行深入阅读

## 第 30 页

**线性注意力层保持固定大小的状态，而不是不断增长的 KV 缓存**

Softmax 注意力：KV 缓存每 token 永远多一条记录

线性注意力：状态 St：dk × dv，每一步大小相同，原地更新

朴素线性注意力：每个 token 把它的 key × value 加到状态上；query 读取该状态

Gated DeltaNet：先让旧状态衰减，再覆盖新 key 指向的内容

Qwen3-Next：48 层 —— GDN GDN GDN Attn ×12 —— 36 层 Gated DeltaNet + 12 层注意力；只有这 12 层保留 KV 缓存

αt：衰减门，忘记多少

βt：写入门，覆盖的力度

同样的 3∶1 配方：Kimi Linear、Qwen3.5

服务效果：4 层中有 3 层在任意上下文长度下都为每个请求保持恒定大小的状态

Yang et al., Gated Delta Networks, ICLR 2025; Qwen Team, Qwen3-Next, 2025

ADVANCED —— 可略读，或自行深入阅读

## 第 31 页

**状态空间模型同样保持固定大小的状态**

Selective（选择性）：Ā 和 B̄ 依赖每个 token，因此该层自己选择保留什么

Fixed state（固定状态）：每个通道保留一个小状态 h，因此 n 增长时解码内存保持平坦

服务效果：没有不断增长的 KV 缓存；Mamba 报告生成吞吐最高可达 Transformer 的 5×

Gu & Dao, Mamba, COLM 2024; Dao & Gu, Mamba-2, ICML 2024

| | 门控线性注意力 | 状态空间（Mamba） |
| --- | --- | --- |
| 更新 | S ← α S + β v kᵀ | h ← Ā h + B̄ x |
| 状态 | 一个 dk × dv 的矩阵 S，存键值对 | 每个通道一个小向量 h |
| 每个 token 做什么 | 把它的 value × key 加到 S，并按 β 缩放 | 用 Ā 让 h 衰减，再加 B̄ × token x |
| 遗忘门 | α：由 token 决定 S 衰减多少 | Ā：由 token 决定 h 衰减多少 |
| 根源 | 没有 softmax 的注意力 | 信号处理与 RNN |

硬件友好的扫描：并行扫描把状态留在 SRAM 中；Mamba-2 把它变成矩阵乘

ADVANCED —— 可略读，或自行深入阅读

## 第 32 页

**稀疏注意力每个查询只读取前 2,048 个过去的 token**

Indexer 为每个过去 token 打分：1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16

图中以 16 个 token 中 k = 4 为例；DeepSeek-V3.2 保留 k = 2,048

1. Score：I_{t,s} = Σⱼ w_{t,j} · ReLU(q_{t,j} · k_s)
2. Select：S_t = I_{t,s} 的 top-k
3. Attend：o_t = Attn(q_t, {c_s : s ∈ S_t})

Indexer：少量头，FP8，每个 token 一个 128 个数的 key

主注意力：2,048 个 token，而不是全部 n 个

服务效果：每个 token 的工作量上限为 2,048 次读取，但所有 token 的 KV 仍然存储

深红 = top-k，被选中参与注意力

DeepSeek-AI, DeepSeek-V3.2-Exp, 2025

ADVANCED —— 可略读，或自行深入阅读

## 第 33 页

**循环 Transformer 多次复用同一个块，所以深度花的是计算，不是权重**

共享权重：一个块 R 被应用 K 次，因此额外深度不增加参数

测试时的深度：一个 3.5B 的循环深度模型在推理任务上随着 K 增长而变好

系统权衡：权重保持很小，但每次循环都是串行的：延迟随 K 增长

无参数的计算：K 次循环消耗该块 FLOPs 的 K 倍，且不额外占用权重内存

Input → Prelude P → Block R × K → Coda C → Output

每次循环权重相同：更多循环增加计算和延迟，而不增加参数

Dehghani et al., Universal Transformers, ICLR 2019; Geiping et al., 2025

ADVANCED —— 可略读，或自行深入阅读

## 第 34 页

**扩散语言模型通过少数几个并行细化步骤填充被遮蔽的 token**

深红轮廓 = 在这一步被填入

Step 0　[M] [M] [M] [M] [M] [M]

Step 1　[M] read [M] weight [M] [M]

Step 2　GPUs read [M] weight [M] step

Step 3　GPUs read every weight each step

LLaDA（2025）：8B 掩码扩散模型，从零开始在 2.3T token 上训练；与 Llama 3 8B 相当

Dream 7B（2025）：从 Qwen2.5 7B 的权重出发；网络仍然是 Transformer

服务效果：一次前向填充多个 token，但步骤越少质量越低

Nie et al., LLaDA, 2025; Ye et al., Dream 7B, 2025

ADVANCED —— 可略读，或自行深入阅读

## 第 35 页

**下一讲**

## 第 36 页

**延伸阅读**
