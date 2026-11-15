---
title: "9_llm_serving_basics_1"
source: https://cs2680.seas.harvard.edu/slides/9_llm_serving_basics_1.pdf
pages: 36
crawled: 2026-11-16
---

# 9_llm_serving_basics_1

> PDF 讲义文本抽取：[9_llm_serving_basics_1.pdf](https://cs2680.seas.harvard.edu/slides/9_llm_serving_basics_1.pdf) · Harvard CS2680

Modern AI Systems: Agents 
and System Optimizations
Juncheng Yang
LLM Serving Basics I: Introduction to LLM 

2Harvard MaDSys    ·   course.agentic-system.org 2
Logistics
• Assignment 3 due on Tuesday 11:59pm
• NO LATE DAY for leaderboard submission
• Check website for what needs to be submitted
• Project poster presentation option 2: 1-3pm Dec 2
• only sign up if you cannot attend on Dec 7
• signup due last Sunday, send us an email ASAP if you want to present on 
Dec 2

3Harvard MaDSys    ·   course.agentic-system.org 3
Plan for today
• Introduction to LLM
• lifecycle of an LLM request
• transformer architecture[1] 
• dense, MoE and advanced variants
• Introduction to GPU for LLM serving[2]
• GPU basics
• GPU architecture
• GPU programming and recent kernel advances
[1] This lecture assumes traditional self-attention transformer architecture
[2] We will not go into details; the goal is to help you build intuition

4Harvard MaDSys    ·   course.agentic-system.org 4
Lifecycle of an LLM request
Six stages from prompt to streamed text. 
1
Tokenize
2
Schedule
3
Prefill
4
Decode
5
Detokenize
6
Stream
repeat per output token
Prefill → time to first token
whole prompt in one forward pass
Decode → tokens per second
one forward pass per output token

5Harvard MaDSys    ·   course.agentic-system.org 5
Stage 1: Tokenization
• Text is split into tokens, not words
• About 3–4 characters per token
• Token count drives cost and memory
• Tokenizers differ across models
“Serving is hard”
Serv ing is hard
1841 288 374 2653
4 tokens — not 3 words
Byte-level BPE: start from the 256 byte values, then repeatedly merge the most frequent adjacent pair 
into a new token. No unknown tokens.

9Harvard MaDSys    ·   course.agentic-system.org 9
Stage 2: Scheduling and batching
• Requests arrive independently; 
GPUs want batches
• The scheduler picks who runs 
each step
• Continuous batching: join or leave 
mid-flight
• Admission is capped by KV cache 
memory
step t
R1
R2
R3
free
step t+1
R1
free
R3
R4
step t+2
R1
R5
R3
R4
Finished requests leave, new ones join — no 
waiting for a full batch

10Harvard MaDSys    ·   course.agentic-system.org 10
Stage 3: Prefill
• Whole prompt runs in one pass
• All prompt tokens attend in parallel
• Compute-bound; cost grows with length
• Generate the KV cache, emits token 1
prompt tokens
t1 t2 t3 t4 t5 t6
one forward pass over all tokens
first output token
Compute-bound → time to first token

11Harvard MaDSys    ·   course.agentic-system.org 11
Stage 4: Decode generates logits; sampling 
picks the next token
STAGE 4 · DECODE
step 1 KV
step 2 KV
step 3 KV
step 4 KV
One forward pass per new token
Cache grows by one token per step
Bandwidth-bound, so batch it
Cache full → preempt or queue
STAGE 5 · SAMPLING
Temperature   temperature = 0
0: always the top token, >1: more tokens are possible
Top-k   top_k = 50
Sample from the k most likely; k is fixed
Top-p (nucleus)   top_p = 0.9
Fewest tokens summing to p; adapts to confidence
Same model, same prompt: these settings change the answer and how long it runs

12Harvard MaDSys    ·   course.agentic-system.org 12
Stage 5: Detokenize and stream
• Token IDs become text as produced
• Partial characters are buffered
• Streaming makes it interactive
• Stopping early frees cache memory
what the user sees, token by token
t1 The
t2 The model
t3 The model streams
t4 The model streams tokens
Stop token, length limit or disconnect ends 
the stream

13Harvard MaDSys    ·   course.agentic-system.org 13
Lifecycle: what to take away
1  Tokenize: turns text into token IDs; a bigger vocabulary means fewer tokens but a larger 
embedding table.
2  Schedule: continuous batching lets requests join and leave every step; KV cache memory 
caps admission.
3  Prefill: the whole prompt runs in one compute-bound pass, generates the KV cache and 
the first token.
4  Decode and sample: one memory-bound forward pass per token; sampling picks each 
token from the logits.
5  Detokenize and stream: turn each token ID into text and send it as it is produced.

Harvard MaDSys    ·   course.agentic-system.org 14
Peeking into the model

15Harvard MaDSys    ·   course.agentic-system.org 15
Notation
MODEL SHAPE WORKLOAD AND MEMORY
Symbol Meaning Llama 3 70B
d model width 8,192
L layers 80
H query heads 64
Hkv key/value heads 8
dk head dimension, d ÷ H 128
dff MLP hidden width 28,672
V vocabulary size 128,256
Symbol Meaning Llama 3 70B
n tokens in the sequence e.g. 20,000
B concurrent requests e.g. 16
N parameters 70.6B
W weight bytes (BF16) 141 GB
KV KV bytes per token 320 KB
KV = 2 × L × Hkv × dk × 2 B
Kᵀ is K transposed
Meta, The Llama 3 Herd of Models, 2024

16Harvard MaDSys    ·   course.agentic-system.org 16
An LLM is a stack of identical transformer 
blocks
token IDs Input: text arrives as integer token IDs
Embedding Embedding: each ID becomes a vector (8,192-dim)
Transformer block  × L L = 80 blocks in Llama 3 70B, each with norm + residual
Self-attention Attention: mixes information across tokens
Feed-forward (FFN) FFN: transforms each token on its own
LM head LM head: one score per vocabulary token
next-token probabilities Softmax: scores become probabilities
Meta, The Llama 3 Herd of Models, 2024

17Harvard MaDSys    ·   course.agentic-system.org 17
Each block adds attention and an MLP to a 
residual stream, each after RMSNorm
ℎ = 𝑥 + Attn RMSNorm 𝑥
𝑦 = ℎ + FFN RMSNorm ℎ
RMSNorm 𝑥  = 𝑥
1
𝑑σ𝑖𝑥𝑖2 + 𝜀
 ⊙ 𝑔
RMSNorm
rescales by the root-mean-
square; one learned gain g per 
dimension
Pre-norm
normalize each sublayer's 
input, so deep stacks train 
stably
Residual stream
x flows through all 80 blocks; 
each sublayer only adds an 
update
Zhang & Sennrich, RMSNorm, NeurIPS 2019; Xiong et al., ICML 2020; Meta, Llama 3, 2024

18Harvard MaDSys    ·   course.agentic-system.org 18
Self-attention lets each token read every 
earlier token
• Each token emits a query, a key and a 
value
• Query · key scores decide how much to 
read from each token
• A causal mask hides future tokens
• n tokens → n² scores: cost grows with 
context
softmax ൗ𝑄𝐾T 𝑑𝑘 ·𝑉
key →
query ↓ The
The
cat
cat
sat
sat
on
on
the
the
0.1 0.2 0.5 0.2 = 1
masked
Vaswani et al., Attention Is All You Need, NeurIPS 2017
Why divide by 𝐝𝐤?
q · k sums dₖ products, so it grows with dₖ; scaling 
keeps softmax from saturating

19Harvard MaDSys    ·   course.agentic-system.org 19
Each token is a row of X; weight matrices turn 
it into Q, K and V
The
cat
sat
on
the
X WQ Q
× =
n × d d × dk n × dk
Q = X WQ   what each token looks for
K = X WK   what each token offers
V = X WV   what each token passes on
Variables
n
tokens so far (prompt + output)
d
numbers per token vector (8,192)
dk
numbers per query or key, one head (128)
WQ, WK, WV
learned weights, d × dₖ each, per head
head
one attention unit; 64 run in parallel
Vaswani et al., Attention Is All You Need, NeurIPS 2017

20Harvard MaDSys    ·   course.agentic-system.org 20
Q Kᵀ scores every pair of tokens; softmax 
turns each row into weights
Q
×
KT
=
S
n × dk dk × n n × n
÷ dk, add M, softmax
A
×
V
=
O
n × n n × dv n × dv
One row as an example
Row 4 of A says how much 
token 4 takes from tokens 1 
to 4. The row sums to 1.
Variables
KT  keys turned so each column is 
one token
S  scores: row i, column j = query i · 
key j
M  mask: −∞ above the diagonal 
hides future tokens
A  weights: each row sums to 1
dv  value vector dimension (128)
O  output: each row is a weighted 
mix of V rows
Vaswani et al., Attention Is All You Need, NeurIPS 2017

21Harvard MaDSys    ·   course.agentic-system.org 21
Attention has an O(n2) computation 
complexity
Step Formula Shape
Input X n × d
Queries Q = X WQ n × dk
Scores S=QKT/ dk n × n
Weights A = softmax(S + M) n × n
Output O = A V n × dv
FLOPs per layer
Q KT: 2 n2 d     A V: 2 n2 d
total ≈ 4 n2 d
Memory if S were stored
n2 × heads × layers × 2 B
= 8,1922 × 64 × 80 × 2 B ≈ 690 GB
FlashAttention computes softmax tile by 
tile and never stores S
Vaswani et al., NeurIPS 2017; Dao et al., FlashAttention, NeurIPS 2022

22Harvard MaDSys    ·   course.agentic-system.org 22
Multi-head attention runs 64 small attentions 
in parallel and mixes them with WO
head𝑖 = softmax 𝑄𝑖𝐾𝑖
T
𝑑𝑘
 + 𝑀 𝑉𝑖
MHA 𝑋  = Concat head1,…,head𝐻 𝑊𝑂
Split
Q, K and V split into H = 64 
heads of dₖ = 8,192 ÷ 64 = 128
Attend
each head runs masked 
softmax attention on its own 
128 dimensions
Mix
WO blends the heads into one 
vector
Same FLOPs as one wide head: 64 × 128 = 8,192, so splitting changes what is learned, not the cost
Vaswani et al., Attention Is All You Need, NeurIPS 2017; Meta, Llama 3, 2024

23Harvard MaDSys    ·   course.agentic-system.org 23
Each head attends with its own 128 
dimensions, so heads learn different patterns
INPUT PROJECT ATTEND (5 tokens)
X
n × 8,192
head 1
Q₁ K₁ V₁ · 128 previous token
head 2
Q₂ K₂ V₂ · 128 first token
head 3
Q₃ K₃ V₃ · 128 nearby tokens
head 64
Q₆₄ K₆₄ V₆₄ · 128 whole context
⋮   60 more heads
OUTPUT MIX
head₁
n × 128
head₂
n × 128
head₃
n × 128
head₆₄
n × 128
Concat
n × 8,192
× WO
n × 8,192

25Harvard MaDSys    ·   course.agentic-system.org 25
Sharing key/value heads shrinks the KV cache
Multi-head (MHA)
8 query heads
8 KV heads
1×
KV cache size
Grouped-query (GQA)
8 query heads
2 KV heads
¼×
KV cache size
Multi-query (MQA)
8 query heads
1 KV head
⅛×
KV cache size
KV cache per token = 2 × L × Hkv × dk × bytes per value
Llama 3 70B: 64 query heads share 8 KV heads, so its KV cache is 8× smaller than MHA
= 2 × 80 × 8 × 128 × 2 B = 320 KB per token, vs 2.5 MB with MHA
Ainslie et al., GQA, EMNLP 2023; Shazeer , MQA, 2019

28Harvard MaDSys    ·   course.agentic-system.org 28
Llama 3 70B as an example
d = 8,192
width of a token vector
h = 64,  dh = 128
64 Q heads × 128 = 8,192
hkv = 8
share 8 KV heads
dff = 28,672
FFN hidden width, 3.5 × d
L = 80
transformer blocks in a row
V = 128,256
tokens in the vocabulary
one token = 8,192 numbers (dimension)
KV 1 KV 8
8,192 28,672 hidden units 8,192
1 2 3 4 5 6 7 8 …  80
8,192 128,256 scores, one per vocabulary token
Meta, The Llama 3 Herd of Models, 2024

29Harvard MaDSys    ·   course.agentic-system.org 29
Llama 3 70B: where the parameters sit
Meta, The Llama 3 Herd of Models, 2024
Component Formula Params
Attention / layer 2d · H · dk + 2d · Hkv · dk 151M
FFN / layer 3 · d · dff 705M
All layers 80 × 856M 68.5B
Embed + LM head 2 · V · d 2.1B
Total 70.6B

30Harvard MaDSys    ·   course.agentic-system.org 30
Systems intuition: weights, compute and KV 
cache set prefill, decode and memory
Quantity Formula 1 request 64 requests
Prefill (80K tokens) B · (2N·n + 2L·d·n²) ÷ FLOP/s 9.95 s 637 s
VRAM needed W + B·n·KV 167 GB 1,779 GB
Meta, The Llama 3 Herd of Models, 2024; NVIDIA, H200 datasheet, 2024
Weights
2 B × params
141 GB
Compute
≈ 2 × params
141 GFLOPs/token
KV cache
2 × L × Hkv × dk × 2 B
320 KB/token
Llama 3 70B, BF16, on 2× H200: 1,978 TFLOP/s, 9.6 TB/s, 282 GB;  n = 80,000 tokens,  B = requests
How do you support longer sequences?

35Harvard MaDSys    ·   course.agentic-system.org 35
MoE replaces each block's FFN with a router 
and a set of smaller expert FFNs
Shazeer et al., MoE, ICLR 2017; Jiang et al., Mixtral of Experts, 2024
Dense block
Attention
FFN
one large MLP
all of it runs for every token
replace FFN
MoE block
Attention
Router picks top-2
E0 E1 E2 E3 E4 E5 E6 E7
weighted sum
8 smaller FFNs; only 2 run per token

36Harvard MaDSys    ·   course.agentic-system.org 36
Dense vs MoE: memory scales with total 
parameters, compute with active
Model Experts Total Active / token Weights (BF16) GFLOPs / token
Llama 2 70B all (dense) 69B 69B 138 GB 138
Mixtral 8x7B 2 of 8 46.7B 12.9B 93 GB 26
Llama 3.1 405B all (dense) 405B 405B 810 GB 810
DeepSeek-V3 9 of 257 671B 37B 1,342 GB 74
Same quality, less compute: Mixtral matches Llama 2 70B at ~1/5 the FLOPs; DeepSeek-V3 
rivals Llama 3.1 405B at ~1/11 the FLOPs but needs 1.7× the memory.
GFLOPs ≈ 2 × active params. Jiang et al. 2024; DeepSeek-AI 2024; Touvron et al. 2023; Llama T eam 2024

Harvard MaDSys    ·   course.agentic-system.org 37
Advanced LLMs
Sliding window
Multi-Latent attention
Linear attention
State-space models
Sparse attention
Looped transformers
Multi-token prediction
Diffusion LMs
ADVANCED — skim, or read more on your own

38Harvard MaDSys    ·   course.agentic-system.org 38
Sliding-window layers cap the KV cache; a 
few global layers keep long-range recall
Full causal Sliding window, w = 3
last token reads all
KV grows with n
last token reads 3
KV capped at w tokens
Gemma 3 layer pattern
L L L L L G
5 local (w = 1,024) to 1 global, repeated
Mistral 7B
every layer local, w = 4,096
Gemma 2
alternates 1 local (w = 4,096) : 1 global
Serving effect: at 128K context, Gemma 3 stores about 6× less KV than all-global layers
Gemma Team, Gemma 3 Technical Report, 2025
ADVANCED — skim, or read more on your own

39Harvard MaDSys    ·   course.agentic-system.org 39
MLA stores one compressed latent per token
token h compress latent c · cached expand to K, V
Store the summary, rebuild the details: K and V are recomputed from c when attention needs them
Extra math, less memory
the up-projection is folded into 
the query and output weights at 
decode time
Serving effect: vs. DeepSeek 67B, DeepSeek-V2 cuts KV cache 93% and lifts generation throughput 5.8×
DeepSeek-AI, DeepSeek-V2, 2024; DeepSeek-AI, DeepSeek-V3, 2024
MHA caches K and V for every head MLA caches one latent c
t1 t1 c
t2 t2 c
t3 t3 c
blue = K, yellow = V, 8 of 128 heads shown; dashed = rebuilt from c, never stored
ADVANCED — skim, or read more on your own

40Harvard MaDSys    ·   course.agentic-system.org 40
Linear-attention layers keep a fixed-size state 
instead of a growing KV cache
Softmax attention
KV cache: one more entry
per token, forever
Linear attention
state St: dk × dv
same size at every step,
updated in place
Plain linear attention
each token adds its key × value to the state; a query 
reads the state
Gated DeltaNet
first fade the old state, then overwrite what the new key 
points to
Qwen3-Next: 48 layers
GDN GDN GDN Attn ×12
36 Gated DeltaNet + 12 attention;
only the 12 keep a KV cache
αt  decay gate: how much to forget
βt  write gate: how hard to overwrite
Same 3:1 recipe: Kimi Linear, Qwen3.5
Serving effect: 3 of 4 layers hold a constant-size state per request, at any context length
Yang et al., Gated Delta Networks, ICLR 2025; Qwen Team, Qwen3-Next, 2025
ADVANCED — skim, or read more on your own

41Harvard MaDSys    ·   course.agentic-system.org 41
State-space models also keep a fixed-size state
Selective
Ā and B̄  depend on each token, 
so the layer chooses what to 
keep
Fixed state
each channel keeps a small 
state h, so decode memory 
stays flat as n grows
Serving effect: no growing KV cache; Mamba reports up to 5× a Transformer's generation throughput
Gu & Dao, Mamba, COLM 2024; Dao & Gu, Mamba-2, ICML 2024
Gated linear attention State-space (Mamba)
Update S ← α S + β v kᵀ h ← Ā h + B̄ x
State a dk × dv matrix S of key–value pairs a small vector h per channel
Each token adds its value × key to S, scaled by β decays h by Ā, then adds B̄  × token x
Forgetting gate α: the token sets how much S decays Ā: the token sets how much h decays
Roots attention without the softmax signal processing and RNNs
ADVANCED — skim, or read more on your own
Hardware-aware scan
a parallel scan keeps the state 
in SRAM; Mamba-2 turns it into 
matmuls

43Harvard MaDSys    ·   course.agentic-system.org 43
Sparse attention reads only the top 2,048 past 
tokens per query
Indexer score for each past token
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
Shown with k = 4 of 16 tokens; DeepSeek-V3.2 keeps k = 2,048
1 Score  It,s = Σj wt,j · ReLU(qt,j · ks)
2 Select  St = top-k of It,s
3 Attend  ot = Attn(qt, {cs : s ∈ St})
Indexer: few heads, FP8, a 128-number key per 
token
Main attention: 2,048 tokens instead of all n
Serving effect: work per token is capped at 2,048 reads, but all tokens' KV stays stored
crimson = top-k, selected for attention
DeepSeek-AI, DeepSeek-V3.2-Exp, 2025
ADVANCED — skim, or read more on your own

45Harvard MaDSys    ·   course.agentic-system.org 45
Looped transformers reuse one block many 
times, so depth costs compute, not weights
Shared weights
one block R is applied K times, 
so extra depth adds no 
parameters
Depth at test time
a 3.5B recurrent-depth model 
gets better on reasoning tasks 
as K grows
System tradeoffs
weights stay small, but each 
loop is sequential: latency 
grows with K
Compute without parameters: K loops cost K× the block's FLOPs and no extra weight memory
Dehghani et al., Universal Transformers, ICLR 2019; Geiping et al., 2025
Input Prelude P Block R  × K Coda C Output
Same weights every loop: more loops add compute and latency, not parameters
ADVANCED — skim, or read more on your own

47Harvard MaDSys    ·   course.agentic-system.org 47
Diffusion LMs fill in masked tokens over a few 
parallel refinement steps
crimson outline = filled in at this step
Step 0 [M] [M] [M] [M] [M] [M]
Step 1 [M] read [M] weight [M] [M]
Step 2 GPUs read [M] weight [M] step
Step 3 GPUs read every weight each step
LLaDA (2025)
8B masked-diffusion model trained 
from scratch on 2.3T tokens; 
competitive with Llama 3 8B
Dream 7B (2025)
Starts from Qwen2.5 7B weights; 
the network is still a Transformer
Serving effect: one pass fills many tokens, but fewer steps cost quality
Nie et al., LLaDA, 2025; Y e et al., Dream 7B, 2025
ADVANCED — skim, or read more on your own

50Harvard MaDSys    ·   course.agentic-system.org 50
Next class

Harvard MaDSys    ·   course.agentic-system.org 51
Optional reading
