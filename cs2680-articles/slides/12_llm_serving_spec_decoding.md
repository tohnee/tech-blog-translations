---
title: "12_llm_serving_spec_decoding"
source: https://cs2680.seas.harvard.edu/slides/12_llm_serving_spec_decoding.pdf
pages: 78
crawled: 2026-11-16
---

# 12_llm_serving_spec_decoding

> PDF 讲义文本抽取：[12_llm_serving_spec_decoding.pdf](https://cs2680.seas.harvard.edu/slides/12_llm_serving_spec_decoding.pdf) · Harvard CS2680

Modern AI Systems: Agents 
and System Optimizations
Juncheng Yang
LLM Serving: Speculative Decoding 

2Harvard MaDSys    ·   course.agentic-system.org
Logistics
• Course Overview
• Last serving lecture (Nov 4): batching, paging and parallelism
• Today: speculative decoding; next: KV cache, then quantization
• Logistics
• Assignment 5 (Mads-Stack) is out today; due Tue, Nov 24, 11:59 pm
• Wed, Nov 18: showcase your Assignment 4 serving engine
• No class Wed, Nov 25 (Thanksgiving recess)

3Harvard MaDSys    ·   course.agentic-system.org
Plan for today
• Foundation of speculative decoding
• Drafter
• Verification
• Systems

4Harvard MaDSys    ·   course.agentic-system.org
Foundations
• why decoding is slow
• draft, verify, accept
• rejection sampling and exactness
• the arithmetic of speedup

5Harvard MaDSys    ·   course.agentic-system.org
Decoding is memory-bound
GPU memory (HBM) Memory bus Compute cores Output
Model weights
16 GB
Llama-3-8B, FP16
4.8 TB/s
≥3.3 ms
per token
~1 FLOP per byte loaded
needs ~206 to stay busy
1 token
per sequence
“sat”
Tokens come out one at a time: each step waits for the one before
Step 1: “The”
re-reads 16 GB
Step 2: “cat”
re-reads 16 GB
Step 3: “sat”
re-reads 16 GB
Step 4: “on”
re-reads 16 GB
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup
Question: The cores sit idle while weights stream in. What could use that compute?

6Harvard MaDSys    ·   course.agentic-system.org
Draft cheaply, verify in parallel
Autoregressive
1 token per pass
Speculative
1 to k+1 per round
target pass
+1
target pass
+1
target pass
+1
target pass
+1
verify pass
+4
verify pass
×
+1
verify pass
×
+3
time
1 Draft: a small model 
guesses k tokens
2 Verify: the big model 
checks all k at once
3 Accept: accept the right 
guesses, add one token
draft (k = 3) accepted × rejected discarded from target
In the same time, speculative decoding makes 8 tokens (4 + 1 + 3) instead of 4.
Fast Inference from Transformers via Speculative Decoding
Accelerating Large Language Model Decoding with Speculative Sampling
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup
Question: The drafter is a weaker model. How can the output still match the target?

7Harvard MaDSys    ·   course.agentic-system.org
Rejection sampling makes cheap guesses exact
Example: p(x) = 3x² on [0, 1]
Draw X, U uniform on [0, 1]; keep X if U ≤ X².
U
x = 0.2
keep 4%
x = 0.8
keep 64%
keep: U ≤ X² retry: U > X²
Kept X has density
∝ x².
Over [0, 1] the 
integral of x² is ⅓, so 
normalizing gives 3x².
Red is a third of the 
square: 1 in 3 kept.
General rule
Pick a proposal q you can sample and a 
constant M with p(x) ≤ M·q(x) for all x.
Draw X ~ q; keep it with chance p(X) / (M·q(X)). 
Otherwise, retry.
Why it works
𝑞(𝑥) × 𝑝(𝑥)
𝑀𝑞(𝑥) = 𝑝(𝑥)
𝑀
How often x is proposed × chance it is kept 
leaves p(x)/M, so kept samples follow p. 1 in M 
draws is kept: a q close to p wastes fewer.
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

8Harvard MaDSys    ·   course.agentic-system.org
Rejection sampling works on tokens
With M = 2, blue covers red
proposed: 2 × q wanted: p
0.6
“cat”
keep all
1.2
“dog”
keep 1 in 4
0.2
“rat”
keep 1 in 2
Throw away the pale part; red is left.
1 Propose: the draft model q picks a word.
2 Check: keep it with chance red ÷ blue:
p(x) / (2·q(x)).
3 Retry: if it is thrown away, pick again.
Same rule, M = 2: kept words follow p, at 2 
picks per word on average.
Speculative decoding’s version
It drops the ×2: keep a draft token with chance min(1, 
p/q). No retry: on a rejection, sample from p, so every 
round makes a token.
Various Techniques Used in Connection with Random Digits
Fast Inference from Transformers via Speculative Decoding
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

9Harvard MaDSys    ·   course.agentic-system.org
Each round drafts, verifies and accepts
1 Draft: the small drafter q guesses k 
tokens x̃1 … x̃k, one at a time. The tilde 
marks a guess.
2 Verify: one pass of the big target p scores 
all k guesses, plus one position after them.
3 Accept: accept each x̃i with chance (1), 
left to right. At the first rejection, resample 
from (2) and stop.
4 Bonus: if all k guesses survive, take one 
more token from the target’s last pass. It is 
free.
(1) Accept a guess
(2) Resample after a rejection
accept  𝑥𝑖 with probability min 1,𝑝  𝑥𝑖
𝑞  𝑥𝑖
p(x) and q(x) are each model’s chance of token 
x. If p ≥ q, always accept.
𝑥 ~ 𝑝′ 𝑥  = max 0,𝑝 𝑥  − 𝑞 𝑥
 𝑥′max 0,𝑝 𝑥′  − 𝑞 𝑥′
Tokens p wants more than q offered, rescaled to 
sum to 1. 
Fast Inference from Transformers via Speculative Decoding
Accelerating Large Language Model Decoding with Speculative Sampling
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

10Harvard MaDSys    ·   course.agentic-system.org
Accept with probability min(1, p/q)
accept chance = min 1,𝑝  𝑥
𝑞  𝑥
If the target likes the guess at least as 
much as the drafter, always accept.
Example: a vocabulary of three tokens; the drafter guesses one of them.
token target p drafter q accept chance why
“cat” 0.6 0.3 1 q < p: always accept
“dog” 0.3 0.6 ½ q > p: accept 1 in 2
“rat” 0.1 0.1 1 q = p: always accept
Takeaway: only over-guessed tokens (“dog”) get rejected, and only by the amount q exceeds p.
Fast Inference from Transformers via Speculative Decoding
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

11Harvard MaDSys    ·   course.agentic-system.org
Rejected tokens are resampled from the leftover
𝑝′ 𝑥  = max 0,𝑝 𝑥  − 𝑞 𝑥
 𝑥′max 0,𝑝 𝑥′  − 𝑞 𝑥′
After a rejection, draw only from 
tokens the target wanted more than q 
offered. Same cat / dog / rat 
example.
1  Leftover: max(0, p − q) 2  Rescale to sum to 1 3  Why it fits
cat 0.3
dog 0
rat 0
total leftover = 0.3
cat 1.0
dog 0
rat 0
0.3 ÷ 0.3: all on “cat”
Accept rate α = Σ min(p, q) = 
0.3 + 0.3 + 0.1 = 0.7
Rejections happen 1 − α = 
0.3 of the time, the same 0.3 
as the leftover total.
So resampling adds exactly 
the leftover: +0.3 to “cat”.
Takeaway: the resample refills exactly the probability that rule (1) rejected.
Fast Inference from Transformers via Speculative Decoding
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

12Harvard MaDSys    ·   course.agentic-system.org
Accepted plus resampled equals p
Pr emit 𝑥  = min 𝑝 𝑥 ,𝑞 𝑥  + max 0,𝑝 𝑥  − 𝑞 𝑥  = 𝑝 𝑥
Chance each token comes out, by path Check each token
cat:  0.3 + 0.3 = 0.6 = p ✓
dog:  0.3 + 0 = 0.3 = p ✓
rat:  0.1 + 0 = 0.1 = p ✓
Same totals as the target p.
All teal = α: 0.3 + 0.3 + 0.1 = 0.7
Takeaway: for every token the two paths add back to p, so the output follows p exactly.
Fast Inference from Transformers via Speculative Decoding
0.3 0.3
0.3
p = 0.6
p = 0.3
p = 0.1
cat dog rat
Guess accepted Resampled
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

13Harvard MaDSys    ·   course.agentic-system.org
Speculative decoding is exact
A token x can come out two ways: guessed and accepted, or rejected and resampled as x.
Pr emit 𝑥 = min 𝑝 𝑥 ,𝑞 𝑥 + max 0,𝑝 𝑥  − 𝑞 𝑥 = 𝑝 𝑥
guess x accepted rejected, then resampled as x target p’s chancechance x comes out
When q(x) < p(x): drafter too cautious
q(x) p − q
All of q(x) is accepted; resampling adds p − q.
When q(x) > p(x): drafter too eager
p(x) q − p
Only p(x) is accepted; the extra q − p is rejected.
Fast Inference from Transformers via Speculative Decoding
Accelerating Large Language Model Decoding with Speculative Sampling
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup
Question: The output is exact. But what does checking k extra tokens cost?

15Harvard MaDSys    ·   course.agentic-system.org
Verification cost is low
3.3 ms
knee
16.6 ms
0
5
10
15
20
1 256 512 768 1024
Time per pass, ms, by tokens in the pass
Llama-3-8B FP16 on one H200, ideal roofline T(n) ≈ max(W / B,  n·W / F)
n  tokens per pass B  bandwidth, 4.8 TB/s
W  weights, 16 GB F  compute, 989 TFLOPS
k  drafts per request batch  requests per pass
The knee is n = F / B ≈ 206
Each weight costs 2 bytes and 2 FLOPs per 
token, so n tokens cost n·W FLOPs.
Batch and k share the budget
n = batch × (k + 1) ≤ 206 stays free: k ≤ 5 at 
batch 32, k ≤ 2 at 64, none from 128.
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

16Harvard MaDSys    ·   course.agentic-system.org
Acceptance rate sets the speedup
α  chance a draft token is accepted
k  draft length per round
c  draft step cost ÷ target step cost
Expected tokens per target pass
E = 1 + α + … + αᵏ = (1 − αk+1) / (1 − α)
Speedup over plain decoding
S = E / (ck + 1)
Example: α = 0.8, k = 4, c = 0.05 gives 
E ≈ 3.4 and S ≈ 2.8×
Expected tokens per target pass
by draft length k, for three acceptance rates α
Fast Inference from Transformers via Speculative Decoding
6.1 α = 0.9
4.3 α = 0.8
2.5 α = 0.6
0
1
2
3
4
5
6
7
1 2 3 4 5 6 7 8
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

17Harvard MaDSys    ·   course.agentic-system.org
Drafting further has diminishing returns
As k → ∞: αk+1 → 0, so E → 1 / (1 − α).
But: each draft step still costs c, so S = E / (ck + 1) peaks, then falls toward 0.
Expected tokens per target pass, E
by draft length k, for three acceptance rates α
Speedup over plain decoding, S
by draft length k, draft cost c = 0.05
Fast Inference from Transformers via Speculative Decoding
α = 0.9
α = 0.8
α = 0.6
0
2.5
5
7.5
10
1 5 10 15 20 25 30
4.7×
α = 0.9
α = 0.8
α = 0.6
0×
1×
2×
3×
4×
5×
6×
1 5 10 15 20 25 30
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

18Harvard MaDSys    ·   course.agentic-system.org
α measures how much p and q overlap
𝛼 =  
𝑥
min 𝑝 𝑥 ,𝑞 𝑥
Each token counts up to the smaller of its 
two chances: α is the probability both 
models share.
Example: the same cat / dog / rat vocabulary.
token target p drafter q shared: min(p, q)
“cat” 0.6 0.3 0.3
“dog” 0.3 0.6 0.3
“rat” 0.1 0.1 0.1
α = 0.3 + 0.3 + 0.1 = 0.7
Greedy decoding
At temperature 0 each 
model puts all its 
chance on one token, so 
α is how often the 
drafter’s top token 
matches the target’s.
Fast Inference from Transformers via Speculative Decoding
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

19Harvard MaDSys    ·   course.agentic-system.org
Smaller drafters gave bigger speedups
3.4×
2.8×
1.7×
T5-small (77M) T5-base (250M) T5-large (800M)
Speedup over T5-XXL (11B) decoding, by drafter
English–German translation, greedy decoding Why the bigger drafters lost
α barely moves: 0.75, 0.80, 0.82.
Draft cost grows 10×: 77M to 800M 
parameters, so c·k eats the gain.
Takeaway: a cheap drafter with decent α beats an accurate but slow one.
Fast Inference from Transformers via Speculative Decoding
Accelerating Large Language Model Decoding with Speculative Sampling
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

20Harvard MaDSys    ·   course.agentic-system.org
Higher temperature lowers the speedup
3.4×
2.6× small2.8×
2.4× base
1.7×
1.4× large
Greedy (T = 0) Sampling (T = 1)
Speedup over T5-XXL (11B) decoding, by drafter
English–German; α fell 0.75→0.62, 0.80→0.68, 0.82→0.71
Fast Inference from Transformers via Speculative Decoding
T = 0 checks one token
Accept iff the draft is argmaxp, so α is 
the top-1 match rate.
T = 1 checks the whole shape
Any mismatch in the distribution 
reduces acceptance.
The best k shrinks too
At T = 1 the best k fell from 7 to 5.
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

21Harvard MaDSys    ·   course.agentic-system.org
Three levers raise the speedup
𝑆 = 𝐸
𝑐𝑘 + 1
E tokens per target pass, set by α and k
c·k cost of the k draft steps, in target steps
1 the verify pass, assumed to cost one decode step
Raise E
Drafters that match p better 
raise α. Token trees try several 
guesses per position. Relaxed 
checks accept near-misses.
Shrink c·k
Reuse the target’s hidden 
states, copy text already 
seen, or draft all k tokens in 
one pass.
Keep the 1 at 1
Checking k + 1 tokens costs 
one decode step only while 
compute sits idle. Large 
batches and MoE models 
break this.
Fast Inference from Transformers via Speculative Decoding
Why decoding is slow Draft, verify, accept Rejection sampling and exactness The arithmetic of speedup

22Harvard MaDSys    ·   course.agentic-system.org
Draft models

23Harvard MaDSys    ·   course.agentic-system.org
Most drafters reuse the target model
Drafts come from Family Examples
A separate model Independent small model T5-small, Llama 3.2 1B
The target’s own layers or 
hidden states
Self-speculation LayerSkip, SWIFT
Prediction heads Medusa
Feature-level drafters EAGLE, EAGLE-2, EAGLE-3
Native multi-token prediction DeepSeek-V3 MTP
Parallel and block drafters DFlash, DSpark
Text already seen Copying and retrieval N-gram lookup, SuffixDecoding
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

24Harvard MaDSys    ·   course.agentic-system.org
DistillSpec trains the drafter to agree
Problem Off-the-shelf small models are trained for quality, not for agreement with a given 
target, so their acceptance rate α is low and caps the speedup.
Motivation α measures how much probability the drafter shares with the target, so a drafter 
distilled to match the target gets a higher α.
Key idea Distill from the target on prefixes the drafter itself samples (on-policy), with a 
divergence chosen per task and decoding strategy.
DistillSpec: Improving Speculative Decoding via Knowledge Distillation
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval
Question: Could the target model draft for itself, with no second model?

26Harvard MaDSys    ·   course.agentic-system.org
LayerSkip drafts with early layers
Problem Speculative decoding usually needs a second model: extra weights and KV 
cache, a matching tokenizer, and a drafter to retrain whenever the target changes.
Motivation Many tokens don’t need every layer, but a normally trained model’s middle layers 
can’t decode through the LM head, so exiting early gives poor drafts.
Key idea Train with layer dropout and an early-exit loss so early layers can predict; draft 
with layers 1 to ℓ, verify with layers ℓ + 1 to L, reusing the drafts’ KV cache.
LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

27Harvard MaDSys    ·   course.agentic-system.org
LayerSkip verifies only the skipped layers
layer ℓ
⋯
layer 1
shared LM 
head
draft ×k
layer L
⋯
layer ℓ + 1
verify
LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding
SWIFT: On-the-Fly Self-Speculative Decoding for LLM Inference Acceleration
cost ≈ k·ℓ/L + (1 − ℓ/L) passes
vs k·c + 1 with a separate drafter
Insights
One model, one cache: no drafter weights or 
second KV cache; verification reuses the KV 
of layers 1..ℓ.
Training makes exits usable: layer dropout 
that rises with depth, plus an exit loss on the 
shared LM head.
Training-free: SWIFT skips middle layers 
instead, chosen by Bayesian optimization.
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

28Harvard MaDSys    ·   course.agentic-system.org
Medusa adds heads that guess ahead
Problem A separate draft model is hard to get and to serve: it must share the tokenizer, 
track the target’s distribution, and run beside it as a second model.
Motivation The last hidden state already carries signal about tokens beyond the next one, 
and small heads on it train cheaply, even with the backbone frozen.
Key idea Add K heads on the last hidden state; head k predicts token t + k + 1. Combine 
each head’s top guesses into a tree and verify it in one pass with tree attention.
Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

29Harvard MaDSys    ·   course.agentic-system.org
Medusa heads lose accuracy with depth
One target pass: every head reads the same h
h
LM head sat t + 1
head 1 on down t + 2
head 2 the a t + 3
head 3 mat rug t + 4
Candidate tree from the heads’ top guesses
Insights
Blind guesses: every head reads the 
same h, so head 3 can’t see heads 1–2’s 
picks; accuracy falls with depth.
Trees recover some accuracy: top 
guesses per head, pruned to the most-
accepted nodes, verified in one pass.
Two training modes: frozen backbone 
(Medusa-1) or joint fine-tuning (Medusa-
2).
Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads
sat
on
down
the
a
mat Kept: the paths 
most often 
accepted on 
calibration data
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval
Question: Later heads cannot see earlier guesses. What if each guess could?

30Harvard MaDSys    ·   course.agentic-system.org
EAGLE drafts from the target’s features
Problem Token-level drafters accept few tokens: small models predict the next token 
poorly, and Medusa’s heads can’t see each other’s guesses.
Motivation
Second-to-top-layer features are more regular than tokens, so they extrapolate 
better, but after sampling the next feature is ambiguous unless the drafter knows 
the chosen token.
Key idea Predict the target’s next feature, not the next token, and give the drafter the 
sampled token so it knows which way the text went.
EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty
EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees
EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time T est
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

31Harvard MaDSys    ·   course.agentic-system.org
Each EAGLE version closed one gap
Li et al.: EAGLE (ICML 2024), EAGLE-2 (EMNLP 2024), EAGLE-3 (NeurIPS 2025); EAGLE-4 Team (2026)
EAGLE-1
ICML 2024
Gap: small drafters 
guess tokens poorly.
Fix: draft features, 
feed back the 
sampled token.
EAGLE-2
EMNLP 2024
Gap: one fixed tree 
for every context.
Fix: grow the tree by 
drafter confidence.
EAGLE-3
NeurIPS 2025
Gap: training never 
saw its own guesses.
Fix: train on its own 
outputs; fuse three 
layers.
EAGLE-4
Preprint 2026
Gap: one tree size for 
every load.
Fix: size each tree 
from measured cost.
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

32Harvard MaDSys    ·   course.agentic-system.org
EAGLE-1 drafter: one layer, fed its own guesses
EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty
Context from target Draft step 1 Draft step 2
Hidden 
state
LM head
Next token
h(How)
LM head
can
h(can)
LM head
I
h(I)
LM head
do
h(do)
LM head
it
Drafter
1 layer
Drafter
1 layer
Target’s hidden state Token sampled by target Drafter’s guess
Pair: each input joins a hidden state with the token that came out of it.
Draft: one decoder layer predicts the next hidden state; the target’s frozen LM head turns it into a token.
Repeat: after the first guess, the drafter feeds back its own predicted hidden states.
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

33Harvard MaDSys    ·   course.agentic-system.org
EAGLE-2 grows a confidence-shaped tree
EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees
Node value = product of drafter confidences on its path
depth 1 depth 2 depth 3
I
am  .70
will  .20
going  .42
not  .14
be  .16
go  .02
to  .38
home  .02
there  .08
fine  .05
Last accepted token Verified: top 6 by value
Drafted but pruned: “not” (.14) beats “there” (.08)
Insights
Confidence ≈ acceptance: the 
drafter is calibrated. 
Expand, then rerank: grow the top-k 
nodes at each depth, then verify the 
m nodes with the highest V (here k = 
2, m = 6; the paper uses k = 10, m = 
48–60).
Same drafter: no retraining; 20–40% 
faster than EAGLE-1.
Context sets the shape: the same 
budget goes deep on predictable text 
and wide where the drafter is unsure.
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

34Harvard MaDSys    ·   course.agentic-system.org
EAGLE-3 fuses low, mid and high layers
EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time T est
The drafter reads three layers of the target
High layer
Mid layer
Low layer
Target model
EAGLE-1 read only the last layer
Fuse
concat, then FC
Fused g
per token
g replaces the last-layer h as the 
drafter’s input.
What EAGLE-3 changes
Predict tokens, not features: 
the feature loss is gone.
Fuse three layers: low, mid and 
high features carry more than the 
top layer.
Train as you infer: later steps 
learn from the drafter’s own 
outputs.
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

35Harvard MaDSys    ·   course.agentic-system.org
EAGLE-3 trains on its own drafted outputs
EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time T est
Drafter’s input sequence during training
EAGLE-1
Loss: match h + token h(How) can h(can) I h(I) do h(do) it
EAGLE-3
Loss: token only g(How) can g(can) I a(I) do a(do) it
Target’s feature (true) Token Drafter’s own output
EAGLE-1: trained only on true hidden states, so later draft steps never practised on their own guesses.
EAGLE-3: from the third position on, it reads its own outputs a(·), exactly what it sees at inference.
Token loss only: with no hidden state to match, the drafter is free to read the fused g.
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

36Harvard MaDSys    ·   course.agentic-system.org
EAGLE-4 sizes each tree from measured cost
EAGLE-4 Team, 2026, EAGLE-4: One Flexible Drafter for All Batch Sizes and Hardware
Same drafter, tree sized to the load
Batch 1: wide and deep Large batch: short chain
Cheaper LM head for the drafter
hidden low-rank head: 
shortlist full head on shortlist
Draft cost down over 40%, full vocabulary kept
Plain decoding Speculation Idle GPU
Insights
Calibrate once: measure verify 
latency by batch, context and tree 
size.
Grow by gain ÷ cost: widen or deepen 
while the ratio stays above a 
threshold.
One drafter, every load: deep trees 
at batch 1 or long context; chains at 
large batch.
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

37Harvard MaDSys    ·   course.agentic-system.org
The LM head outweighs the drafter
EAGLE-4 Team, 2026, EAGLE-4: One Flexible Drafter for All Batch Sizes and Hardware
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval
Weights read per draft step
Llama-3-8B target: hidden 4,096 × vocabulary 128,256
Two-pass head
Hidden state  4,096 numbers
Low-rank head  34M weights
Shortlist  top few hundred
Full-head rows  about 1M weights
Insight: the drafter skips the full 128K-wide product, yet any token can still reach the shortlist.
34M
220M
525M
Low-rank head
Drafter layer
Full LM head

38Harvard MaDSys    ·   course.agentic-system.org
EAGLE was widely used in production
EAGLE trains a small drafter on a frozen target’s features, so a provider can add one to a 
model it already serves.
Meta  Llama 3 and Llama 4
EAGLE in Meta’s serving stack, with online 
distillation, tree attention and batching fixes on 
H100s.
1.4–2.0× faster at large batch
Baseten  custom EAGLE-3 heads
Trains EAGLE-3 heads for customer models. 
1.5–2.5× in production
Efficient Speculative Decoding for Llama at Scale: Challenges and Solutions
How to train custom EAGLE-3 heads for speculative decoding
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

39Harvard MaDSys    ·   course.agentic-system.org
DeepSeek-V3 trains its own drafter
Problem A drafter trained after the fact must chase the target’s distribution, and every new 
model version means training and serving a separate drafter again.
Motivation Predicting further ahead densifies the training signal and may help planning; 
a jointly trained module stays aligned with the main model by design.
Key idea
One sequential MTP module (shared embedding and output head, one 
Transformer block) predicts token t+ 2 during pre-training; 
at inference it serves as a k = 1 drafter.
DeepSeek-V3 Technical Report
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

40Harvard MaDSys    ·   course.agentic-system.org
One draft token caps MTP near 2×
main model, 61 layers output head ti+1
hi
norm, concat, project embed ti+1
1 Transformer block output head ti+2
Crimson: shared with the main model
Blue: new MTP weights, one layer deep
Insights into DeepSeek-V3: Scaling Challenges and Reflections on Hardware for AI Architectures
DeepSeek-V3 Technical Report
Insights
Keeps the causal chain: the module sees 
the true t +1 embedding, unlike Medusa’s 
blind heads.
Near its ceiling: with k = 1, E = 1 +α ≈ 1.9 
at 85–90% acceptance; measured 1.8× 
tokens/s.
Trained with the model: L = Lmain + λ·LMTP 
(λ = 0.3, then 0.1); 14B weights beside 
671B.
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval
Question: Could a drafter propose a whole block of tokens in one pass?

41Harvard MaDSys    ·   course.agentic-system.org
DFlash drafts a block in one pass
Problem Autoregressive drafters such as EAGLE spend k sequential passes to draft k 
tokens, so draft latency grows with k and caps how far ahead it pays to guess.
Motivation Diffusion LMs fill many positions in parallel but lose quality on their own; as 
drafters their mistakes are caught by verification, so only their speed matters.
Key idea A light block-diffusion drafter, conditioned on hidden features fused from several 
target layers, predicts a 16-token masked block in one forward pass.
DFlash: Block Diffusion for Flash Speculative Decoding
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

42Harvard MaDSys    ·   course.agentic-system.org
Long blocks pay off in DFlash
One round with k = 4 drafts (illustrative)
EAGLE-style d1 d2 d3 d4 verify
DFlash d1–4 verify saved
Denoise a masked block in one pass
input t ▢ ▢ ▢ ▢
light diffusion drafter target h
output t d1 d2 d3 d4
Insights
Flat draft cost: all masked positions 
are filled together, so a 16-token block 
costs one draft pass.
Context comes from the target: draft 
layers attend to hidden states fused 
from several target layers.
Trained as it is used: random anchors, 
with the block after each one masked 
and predicted in parallel.
DFlash: Block Diffusion for Flash Speculative Decoding
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

43Harvard MaDSys    ·   course.agentic-system.org
DSpark verifies only the likely prefix
Problem Parallel drafters lose accuracy along the block, so verifying the full block wastes 
target compute that other requests need.
Motivation Whether extra verified tokens pay off depends on each request’s acceptance and 
on current load, so one fixed verification length is wrong for most requests.
Key idea
Add a light sequential head to DFlash’s parallel backbone, a confidence head 
that predicts prefix survival, and a scheduler that sets each request’s verify length 
from load.
DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

45Harvard MaDSys    ·   course.agentic-system.org
In production, block drafters beat MTP
A block drafter fills a whole block in one pass; in production, the question is how much of 
each block is worth verifying under load.
DeepSeek  DSpark in V4
Co-deployed with DeepSeek-V4 Flash and Pro; a 
confidence head sets each request’s verify 
length under live traffic.
60–85% faster per user than MTP-1
DFlash  SGLang, vLLM, TensorRT-LLM
All three engines support it; on vLLM, a DFlash 
checkpoint replaces EAGLE-3 with only a config 
change.
Up to 5.8× on Gemma 4 31B
DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation
Boost Inference Performance up to 15x on NVIDIA Blackwell Using DFlash Speculative Decoding
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval
Question: Agents often repeat text they have seen. Could we draft with no model?

46Harvard MaDSys    ·   course.agentic-system.org
Retrieval-based drafts does not need a model
Problem Agentic workloads emit long, repetitive outputs; model drafters ignore the 
repetition, and n-gram lookup only searches the current prompt.
Motivation Agents repeat text across calls (code edits, SQL, tool calls), so a cache of earlier 
prompts and outputs can predict long continuations at almost no cost.
Key idea
Keep suffix trees over past outputs (global) and the current request on the CPU; 
match the last p tokens and draft a tree of up to α·p tokens, scored by how often 
each continuation appeared.
SuffixDecoding: Extreme Speculative Decoding for Emerging AI Applications
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

47Harvard MaDSys    ·   course.agentic-system.org
Long guesses are nearly free
Past outputs, kept in a suffix tree on the CPU
“fix the bug in parser” (×2),
“fix the bug in lexer”, “fix the test”
New request ends with “fix the”: match p = 2
fix the
bug 3
test 1
in 3
parser 2
lexer 1
Blue: drafted, the highest-count paths up to α·p = 3 
tokens (α = 1.5)
Insights
Free to draft: a CPU tree lookup instead of 
a GPU pass, so c ≈ 0 and long guesses are 
affordable.
Speculate on evidence: longer matches 
earn longer drafts (α·p); with no match, 
decode normally.
History does most of the work: the global 
tree over past requests gives most of the 
gain.
Workload-dependent: up to 5.3× on 
agentic tasks, 2.8× faster than EAGLE-2/3 
there; pair with EAGLE-3 for open chat.
SuffixDecoding: Extreme Speculative Decoding for Emerging AI Applications
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

48Harvard MaDSys    ·   course.agentic-system.org
In production, retrieval-based SD is common
An edit keeps most of the file, so the original is the draft: one pass verifies a long chunk, 
and only the changed spans decode token by token.
Cursor  speculative edits
A 70B model rewrites the whole file; the current 
file supplies the draft, so no draft model runs.
13× faster, ~1000 tokens/s
OpenAI  Predicted Outputs
API callers send the expected output, often the 
current file, as a prediction; matching text 
returns faster.
Rejected tokens are still billed
Insight: The gain scales with how much of the file survives; a full rewrite accepts little of the 
draft and falls back to normal decoding.
Editing Files at 1000 Tokens per Second
Predicted Outputs
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

49Harvard MaDSys    ·   course.agentic-system.org
Most drafters reuse the target model
Drafts come from Family Examples
A separate model Independent small model T5-small, Llama 3.2 1B
The target’s own layers or 
hidden states
Self-speculation LayerSkip, SWIFT
Prediction heads Medusa
Feature-level drafters EAGLE, EAGLE-2, EAGLE-3
Native multi-token prediction DeepSeek-V3 MTP
Parallel and block drafters DFlash, DSpark
Text already seen Copying and retrieval N-gram lookup, SuffixDecoding
Small model Self-speculation Heads Feature-level Native MTP Parallel & block Retrieval

50Harvard MaDSys    ·   course.agentic-system.org
Verification

51Harvard MaDSys    ·   course.agentic-system.org
SpecInfer verifies a tree in one pass
Problem A single draft sequence from one small model is often wrong early, and the first 
rejection throws away every guess after it.
Motivation At small batch the verify pass leaves compute idle, so checking many candidate 
continuations costs about as much as checking one.
Key idea Merge small-model guesses into a token tree, verify every node in one pass with a 
tree mask; multi-step speculative sampling keeps the output exact.
SpecInfer: Accelerating Large Language Model Serving
with Tree-based Speculative Inference and Verification
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

52Harvard MaDSys    ·   course.agentic-system.org
Trees yield longer accepted runs
Chain: one guess per position
The cat is × on the sat +1 token
Tree: top-2 guesses per position
The cat
sat
is ×
on
down ×
on
the mat
+4 tokens
from 6 verified nodes
accepted × rejected discarded from target
Insights
A level passes if any child does: one 
miss no longer ends the round.
Same pass, more tokens: at batch 1, 6 
tree nodes cost the same 3.3 ms pass as 3 
chain drafts (slide 15).
Any shape, one pass: nodes are flattened 
and masked to see only their ancestors 
(next slide).
SpecInfer: Accelerating Large Language Model Serving
with Tree-based Speculative Inference and Verification
Question: Each branch has its own history. How can one pass check them all?
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

53Harvard MaDSys    ·   course.agentic-system.org
One pass checks every branch
The cat
1 sat
2 is
3 on
4 down
5 on
6 the
1 Flatten: append all nodes; position = n + depth.
2 Mask: each node sees the context and its ancestors.
3 Score: one target pass gives p at every node.
4 Walk: keep the longest passing path, e.g. 1 → 3 → 6.
Attention mask: row sees column
ctx 1 2 3 4 5 6
1 sat
2 is
3 on
4 down
5 on
6 the
Siblings never see each other.
SpecInfer: Accelerating Large Language Model Serving with Tree-based Speculative Inference and Verification
5 Compact: copy that path’s KV into slots n+1..n+3.
position n + 1 n + 2 n + 3
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

54Harvard MaDSys    ·   course.agentic-system.org
Ragged batches: one flat pass for all requests
Inside vLLM: Anatomy of a High-Throughput LLM Inference System
Requests this step
A  k = 4 t d1 d2 d3 d4
B  k = 2 t d1 d2
C  k = 0 t speculation off
flatten
One verify batch: 9 tokens
A
t d1 d2 d3 d4
B
t d1 d2
C
t
offsets 0 5 8 9
Request i adds 1 + kᵢ query tokens; varlen attention indexes them by per-request offsets, rebuilt every step.
One target pass
weights read once for all 9 
tokens
Split by offsets
A gets 5 outputs, B 3, C 1
Sample per request
accept or reject each 
request’s own drafts
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

55Harvard MaDSys    ·   course.agentic-system.org
Speculation costs extra compute
2.6×
2.2×
1.8×
1.5×
1.2×
α = 0.5 0.6 0.7 0.8 0.9
Target FLOPs per kept token, vs plain decoding
k = 4 drafts per pass; drafter FLOPs not included cost per kept token = 𝑘 + 1
𝐸
E = (1 − αk+1)/(1 − α) kept per pass
Fast Inference from Transformers via Speculative Decoding
Where the waste goes
At α = 0.8, k = 4: 3.36 of 5 verified 
positions kept, 1.64 thrown away.
Drafter FLOPs add on top
k·Nd/Nt target passes per round: 0.6 for 
1B→ 8B at k = 4.
Insight: Compute-bound, throughput scales by E/(k+1) < 1 for any α < 1, so the best k there 
is 0: k must follow the load, not stay fixed.
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

56Harvard MaDSys    ·   course.agentic-system.org
Sequoia picks the best tree shape
Problem
Fixed tree shapes stop gaining as trees grow, top-k sampling fails at some 
temperatures, and no single tree size fits every GPU.
Motivation Acceptance per child position can be measured once per model pair, so the best 
tree for a node budget is an optimization problem.
Key idea
A dynamic program builds the tree that maximizes expected accepted tokens; 
sampling without replacement keeps verification robust; a profiler picks tree size 
and depth per GPU.
Sequoia: Scalable, Robust, and Hardware-aware Speculative Decoding
Fixed trees plateau
top-k
Top-k misses the sample
GPU A GPU B
No size fits every GPU
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

57Harvard MaDSys    ·   course.agentic-system.org
Size the tree to the GPU
𝐸 ≈  
𝑣∈𝑇
 
𝑢∈path 𝑣
𝑐𝑢 c: drafter
confidence
The cat
sat .60
is .30
on .48
down .09
on .21
the .43
Blue = top 4 kept:
E ≈ .60 + .48 + .43 + .30 = 1.81 per pass
Sequoia: Scalable, Robust, and Hardware-aware Speculative Decoding
EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees
Speculative Decoding, SGLang Documentation
Insights
Greedy works: path values only shrink, 
so the top m nodes form a tree; the DP 
finds up to 33% more tokens.
Log returns: accepted tokens grow 
about logarithmically with size, but 
verify cost grows linearly past the knee.
In SGLang: num-steps = depth, 
eagle-topk = width, 
num-draft-tokens = m.
Question: Exact checks reject correct but different 
tokens. Could we accept them?
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

58Harvard MaDSys    ·   course.agentic-system.org
Lossy speculative decoding: relax the loop
Drafter the old cat sat Target
scores drafts
Keep?
exact test Output
Judge
learned model1 What is drafted
2 What counts as a match 3 Who verifies 4 The test
5 Add a judge
Exact SD drafts tokens, verifies them against the full target. Each numbered point is one way to accept 
more drafts, and each one changes the output distribution.
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

59Harvard MaDSys    ·   course.agentic-system.org
Draft whole reasoning steps
Drafter so x = 4 Target
scores the step
Keep?
score high? Output
Judge
learned model1 What is drafted
2 What counts as a match 3 Who verifies 4 The test
5 Add a judge
Idea: the drafter writes a whole reasoning step. The target or a judge scores it, and only low-scoring 
steps are regenerated.
Methods: SpecReason, Lookahead Reasoning, ConfSpec, SPEC-RL
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

60Harvard MaDSys    ·   course.agentic-system.org
Accept near-duplicate tokens
Drafter the old cat sat Target
prefers kitten
Keep?
close enough? Output
Judge
learned model1 What is drafted
2 What counts as a match 3 Who verifies 4 The test
5 Add a judge
Idea: keep a draft token that is close to the target’s choice, such as “cat” when the target prefers 
“kitten”, or a neighbouring image token.
Methods: LANTERN, grouped SD, speech SSD, Spec-VLA
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

61Harvard MaDSys    ·   course.agentic-system.org
Verify with a cheaper target
Drafter the old cat sat Target
cheaper copy
Keep?
exact test Output
Judge
learned model1 What is drafted
2 What counts as a match 3 Who verifies 4 The test
5 Add a judge
Idea: check drafts against a cheaper copy of the target, with a sparse KV cache or fewer active experts. 
Verification costs less, but the output drifts from the full model.
Methods: Dustin, MoE-Spec
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

62Harvard MaDSys    ·   course.agentic-system.org
Loosen the acceptance test
Drafter the old cat sat Target
scores drafts
Keep?
looser test Output
Judge
learned model1 What is drafted
2 What counts as a match 3 Who verifies 4 The test
5 Add a judge
Idea: replace the exact accept rule with a looser one: keep any draft token the target finds likely 
enough, even when the exact test would reject it.
Methods: Lenience, top-β, typical acceptance
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

63Harvard MaDSys    ·   course.agentic-system.org
Let a judge keep good rejections
Drafter the old cat sat Target
scores drafts
Keep?
exact test Output
Judge
can overrule1 What is drafted
2 What counts as a match 3 Who verifies 4 The test
5 Add a judge
Idea: a small classifier reads the target’s hidden state at a rejected token and keeps the token when the 
mismatch would not hurt the answer.
Methods: Judge Decoding, AutoJudge, SelfJudge, FLy
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

64Harvard MaDSys    ·   course.agentic-system.org
Lossy SD relaxations: five places to accept more
1 What is drafted Draft whole reasoning steps, scored by a reward model or judge
SpecReason, Lookahead Reasoning, ConfSpec, SPEC-RL
2 What counts as a match Accept a near-duplicate token close to the target’s choice
LANTERN, grouped SD, speech SSD, Spec-VLA
3 Who verifies Verify with a cheaper target: sparse KV or fewer experts
Dustin, MoE-Spec
4 The test Loosen the acceptance rule itself
Lenience, top-β, typical acceptance
5 Add a judge A small classifier overrides some rejections
Judge Decoding, AutoJudge, SelfJudge, FLy
SpecInfer Tree attention Exact tree verification Sequoia Lossy SD Judge Decoding

67Harvard MaDSys    ·   course.agentic-system.org
Optimizing Speculative Decoding in Systems

68Harvard MaDSys    ·   course.agentic-system.org
Speculation fits in one engine step
Inside vLLM: Anatomy of a High-Throughput LLM Inference System
Consistent semantics for drafted, verified and accepted spec decode tokens
One request, k = 4: committed last token t draft accepted rejected
1 Draft
drafter q The cat sat on the mat
2 Verify
target p The cat sat on the mat
3 Accept
sampler The cat sat ✓ on ✓ the ✗ mat ✗
4 Commit
scheduler The cat sat on a

69Harvard MaDSys    ·   course.agentic-system.org
Step time: drafts cost nothing until the GPU is busy
NVIDIA, 2024: H200 Tensor Core GPU datasheet (4.8 TB/s HBM3e, 989 TFLOPS dense BF16)
Step time per verify pass, ms, by batch size
ideal H200 roofline, Llama-3-8B FP16, weights only
Flat up to ~206 tokens: each 
pass waits on the 16 GB 
weight read, so 80 tokens 
cost what 16 do.
Past it, every token adds 
time: about 0.016 ms each, 
so 1,280 tokens take 
20.8 ms.3.3 ms 5.2 ms
20.8 ms
k = 4
4.2 ms
k = 0
0
5
10
15
20
25
batch 1 batch 16 batch 64 batch 256
320 tokens: past the ridge

70Harvard MaDSys    ·   course.agentic-system.org
Large batches erase the free compute
Tokens per weight read in one verify pass, k = 4
H200 needs ~206 to stay busy (slide 5); weights only
limit ≈ 206
batch 1 5 tokens
batch 16 80 tokens
batch 64 320 tokens
Below the limit, 5 tokens cost about as much as 1; above it, 
every token adds time.
Optimizing Speculative Decoding for Serving Large Language Models Using Goodput
Per-user vs total speed
Batch 16: k = 4 lifts each user from 299 
to 1,005 tok/s at the same 3.3 ms step.
Batch 64: 320 tokens per pass, 5.2 ms: 
647 tok/s per user, 41K total.
Batch 256: k = 4 stretches the step to 
20.8 ms: 162 tok/s per user and 41K 
total, below k =0’s 241 and 62K.
Ideal H200 roofline, α = 0.8, weights only, 
drafter free.
Insight: Batching and speculation spend the same ~206 free slots: batching buys total 
throughput, speculation buys per-user speed. Splitting them is an SLO choice.
Batch size Long context MoE Run-time k

71Harvard MaDSys    ·   course.agentic-system.org
TurboSpec picks k every step
Problem Under continuous batching, speculation can raise latency: at high request rates 
or low acceptance, verifying rejected drafts takes compute from other requests.
Motivation The best k depends on batch size and acceptance, which change every step, but 
both the accepted length and the batched step time are predictable.
Key idea
Goodput = generated tokens ÷ step time. Predict each request’s accepted length 
from its acceptance history and the step time with a linear model; pick each k to 
maximize goodput.
Optimizing Speculative Decoding for Serving Large Language Models Using Goodput
Batch size Long context MoE Run-time k

72Harvard MaDSys    ·   course.agentic-system.org
TurboSpec runs a goodput loop every step
Optimizing Speculative Decoding for Serving Large Language Models Using Goodput
1 Track α
moving average of 
the acceptance 
rateα
2 Predict E
expected kept 
tokens E(k) for every 
k, including k = 0
3 Predict T
step time T from a 
linear model of 
batched tokens
4 Pick k
the k with the 
highest goodput 
E / T, then run the 
step
next step: update α with what was accepted
What it picks (α = 0.8): batch ≤ 16: k ≈ 5 batch 64: k ≈ 2 batch 256: k = 0
Batch size Long context MoE Run-time k

73Harvard MaDSys    ·   course.agentic-system.org
The best k shrinks as batches grow
2.08×
batch ≤ 161.86×
batch 641.00×
0.42×
batch 256
0.0×
0.5×
1.0×
1.5×
2.0×
2.5×
0 1 2 3 4 5 6 7 8
Goodput vs plain decoding, by drafts per step k
Model: ideal H200 roofline, Llama-3-8B, 1B drafter, α = 0.8 Insights
Optimize goodput, not acceptance: 
Σ Ei(ki) ÷ step time; E from acceptance 
history, step time from a linear model.
The best k shrinks with load: about 5 up 
to batch 16, 2 at batch 64, 0 at 256 in this 
model; SmartSpec saw > 4 at small batch.
Drafting has a cost: each extra draft adds 
a drafter pass (0.52 ms for a 1B model 
here), so even small batches peak.
Never worse than off: at peak load it 
proposes nothing; at light load, up to 3.2× 
lower latency.
Optimizing Speculative Decoding for Serving Large Language Models Using Goodput
Question: Large batches erase the gain. Can 
anything bring speculation back?
Batch size Long context MoE Run-time k

74Harvard MaDSys    ·   course.agentic-system.org
Long context revives speculation
Problem Speculation is thought to pay off only at small batch sizes.
Motivation At long context, KV reads dominate, so large batches stay memory-bound.
Key idea Draft on a fixed-size sparse KV cache; verify on the full cache.
MagicDec: Breaking the Latency-Throughput Tradeoff
for Long Context Generation with Speculative Decoding
Target verifies
full KV cache
Drafter drafts
sparse KV cache
sinks skipped by the drafter recent window
Batch size Long context MoE Run-time k

75Harvard MaDSys    ·   course.agentic-system.org
KV reads are private to each request
MagicDec: Breaking the Latency-Throughput Tradeoff
for Long Context Generation with Speculative Decoding
Weights: one read serves the whole batch
Weights
16 GB
req 1 · 5 tokens
req 2 · 5 tokens
… req 32 · 5 tokens
160 FLOPs per byte
32 requests × 5 tokens share one weight read, so 
batching raises this toward the 206 an H200 
needs to stay busy.
KV cache: each request reads its own
KV 1 GB req 1 · 5 tokens
KV 1 GB req 2 · 5 tokens
… KV 1 GB … req 32 · 5 tokens
20 FLOPs per byte
Each 1 GB at 8K context serves only its own 5 
tokens (4 FLOPs per byte each with GQA), far 
below 206 at any batch size.
Batch size Long context MoE Run-time k

76Harvard MaDSys    ·   course.agentic-system.org
Speedup grows with batch at long context
16 16
34
20.4 GB
50.4 GB
1K context 8K context
Bytes read per decode step, GB
Llama-3-8B, batch 32, one H200
gray: weights · red: KV cache
MagicDec: Breaking the Latency-Throughput Tradeoff
for Long Context Generation with Speculative Decoding
KV read per pass at 8K context
verify all 8K tokens
draft skippedsink window
Draft cost stays flat in context; the drafter can even be the target
Insights
KV reads aren’t shared: batch 32 at 8K reads 34 GB of 
KV vs 16 GB of weights per step.
Attention stays memory-bound: ~4 FLOPs per KV byte 
with GQA, 4(k + 1) with k drafts, ≪ 206.
Gains grow with batch past ~4K tokens: up to 2.51× at 
batch 32–256 (Llama-3.1-8B).Question: Is verifying k tokens still 
cheap for MoE models?
Batch size Long context MoE Run-time k

77Harvard MaDSys    ·   course.agentic-system.org
Cascade turns speculation off for MoE
Problem On MoE models each verified token routes to its own experts, so verifying k drafts 
reads many more weights; always-on speculation slowed requests by up to 1.5×.
Motivation The payoff varies by model and task (Mixtral, k= 3: 39% faster on code, 54% 
slower on math) but stays stable over short windows of a request.
Key idea Utility = token gain ÷ verification cost. Per request, test a few k briefly, then run the 
best k for a longer phase, or turn speculation off when utility falls below 1.
Utility-Driven Speculative Decoding for Mixture-of-Experts
Batch size Long context MoE Run-time k

78Harvard MaDSys    ·   course.agentic-system.org
Short tests limit MoE slowdown
One Mixtral layer, k= 7: 8 experts, 2 per token
decode 1 token
E1 E2 E3 E4 E5 E6 E7 E8 2 experts
verify 8 tokens
E1 E2 E3 E4 E5 E6 E7 E8 ≈7 experts
N(1 − (1 − k/N)n) ≈ 7.2 of 8 (3.6×); ~3× measured, as 
nearby tokens share experts.
Cascade on one request
test run k = 2 test off test
short tests, longer set phases; utility < 1 turns speculation off
Insights
Utility is stable over short windows: a 
brief test predicts the next, longer phase.
Off still costs a little: the drafter keeps 
running so its KV stays current (2–3%).
Finer experts hurt more: 8 tokens read 
7.2× the routed experts in DeepSeek-V3 vs 
3.6× in Mixtral (uniform routing).
Result: worst-case slowdown 5% instead 
of 1.5×; 7–14% more throughput than 
static k.
Utility-Driven Speculative Decoding for Mixture-of-Experts
Batch size Long context MoE Run-time k

79Harvard MaDSys    ·   course.agentic-system.org
Decide k at run time
SmartSpec  batch size
E from acceptance history, T 
from a linear step-time 
model; at peak load it picks 
k = 0.
Up to 3.2× lower latency
Cascade  MoE
Tests k in short phases; utility 
below 1 turns speculation off, 
but the drafter keeps running 
so its KV stays current (2–3%).
Worst case: 5% slower
DSpark  production
A confidence head estimates 
prefix survival; the scheduler 
sets each request’s verify 
length from load profiles.
60–85% faster per user
DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation
Optimizing Speculative Decoding for Serving Large Language Models Using Goodput
Utility-Driven Speculative Decoding for Mixture-of-Experts
Goodput = Σi Ei(ki) / T(Σi (1 + ki)): choose each ki to maximize it.
E: expected kept tokens for request i · T: step time for that many batch tokens
Insight: All three maximize the same goodput and differ only in how they estimate E: 
acceptance history, short trials, or a learned confidence head.
Batch size Long context MoE Run-time k

80Harvard MaDSys    ·   course.agentic-system.org
Every idea pulls one of three levers
S = E
ck + 1
Raise E
Accept more tokens per pass
Train drafters to agree
DistillSpec, EAGLE-3
Try a tree of guesses
SpecInfer, EAGLE-2, Sequoia
Accept near-misses
Judge Decoding
Shrink c·k
Make drafting cheaper
Reuse the target model
LayerSkip, Medusa, EAGLE, MTP
Draft all k in one pass
DFlash, DSpark
Copy text already seen
N-gram lookup, SuffixDecoding
Keep the 1 at 1
Keep verification at one step
Size k to the load
SmartSpec, EAGLE-4
Speculate at long context
MagicDec
Switch it off for MoE
Cascade
Verify the likely prefix
DSpark

81Harvard MaDSys    ·   course.agentic-system.org
Next class
• Mon, Nov 16: Efficient LLM serving: KV-cache optimization and 
model architectures (student-led)
• Wed, Nov 18: Student sharing III: showcase your serving engine 
(Assignment 4)
• Assignment 5 (Mads-Stack: optimize the full stack) is out today; 
due Tue, Nov 24, 11:59 pm

82Harvard MaDSys    ·   course.agentic-system.org
Optional topics
• Lossy speculative decoding
S = E
ck + 1

83Harvard MaDSys    ·   course.agentic-system.org
