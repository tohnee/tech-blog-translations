---
title: "UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"
arxiv: 2609.39972
date: 2026-10-09
source: https://arxiv.org/abs/2609.39972
project: https://github.com/inclusionAI/ubtree
crawled: 2026-10-29
---
# UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding

## Abstract

Speculative decoding accelerates language model inference by verifying multiple draft tokens in a single target-model pass. Recent parallel drafters have achieved breakthrough performance in frontier production models, but their effectiveness deteriorates as the entropy of target distributions increases due to insufficient draft diversity. To overcome this bottleneck without sacrificing parallelism, we introduce UBTree, a parallel drafter that couples a Unigram proposer with a Bigram selector to construct drafting Trees. The unigram proposer is trained with the standard cross-entropy objective to generate candidate tokens independently for each position, while a lightweight bigram selector predicts transition scores between adjacent candidate pairs. Unlike the proposer, the selector is trained with a renormalized KL objective on high-temperature data. This tree-native training broadens the supervision beyond the greedy path, encouraging plausible alternative branches that improve the chance of accepting additional tokens during tree verification. Across seven standardized benchmarks with Qwen3-4B and Qwen3-8B, UBTree achieves an average speedup of 5.845.84–6.94×6.94\times over autoregressive decoding and outperforms DARTree in all 28 comparisons. Production-scale evaluation further demonstrates UBTree’s advantage over frontier baselines such as DSpark.

††footnotetext: \*Equal contribution. †\daggerCorresponding authors.
  
   This work was done during Chumeng’s and Linxuan’s internship at Inclusion AI.

Figure 1: (a) Speedups on Qwen3-8B: Speedup over autoregressive decoding across seven benchmarks on Qwen3-8B instruct at Tinfer=1T\_{\mathrm{infer}}=1.
(b) Speedups on Qwen3.8-27B: Serving speedup in SGLang on Qwen3.8-27B at Tinfer=1T\_{\mathrm{infer}}=1. (c) Long-context acceptance: Acceptance length τ\tau on Ling3-Flash-124B for LongBench-v2 and SWE-bench over different context lengths. UBTree outperforms competing methods across most benchmarks and model scales.

## 1 Introduction

Speculative decoding ([Leviathan et al., 2023](#bib.bib8); [Chen et al., 2023](#bib.bib9)) offers a lossless approach to accelerating large language models (LLMs): a lightweight drafter proposes multiple future tokens, and the target model verifies them together while preserving its output distribution. The benefit of speculative decoding depends not only on the acceptance length of the draft by the target model but also on the computational cost. Longer accepted drafts do not necessarily yield greater speedup if producing them incurs substantial latency.

Recent advances in speculative decoding have been driven by breakthroughs in parallel drafting ([Liu et al., 2026](#bib.bib15); [Chen et al., 2026](#bib.bib5)). While their autoregressive counterparts ([Li et al., 2024b](#bib.bib12); [Li et al., 2026d](#bib.bib6)) condition each draft token sequentially on preceding choices, parallel drafters predict all future positions in a drafting block with a single proposer-backbone forward pass. Parallelism reduces the sequential overhead of using larger proposer backbones which increases the acceptance length. However, parallel drafters lack draft diversity. Consequently, their performance degrades when high-entropy target distributions inherently produce different paths. Moreover, the missing token-wise dependency may worsen the degradation by mixing these different paths. Existing approaches try to complement this drawback by restoring token-wise dependencies to improve precisions of the single-path draft through lightweight autoregressive correction heads ([Huang et al., 2026](#bib.bib7); [Cheng et al., 2026](#bib.bib16)) or intra-backbone designs ([Inco AI, 2026](#bib.bib17)). However, these strategies do not fundamentally solve the diversity bottleneck because there is still only one single draft path covered. This particularly limits the further improvement of parallel drafters and their applications under scenarios with high entropy target distributions ([Devic et al., 2025](#bib.bib47); [Yang et al., 2026](#bib.bib28)). Draft diversity thus becomes a central bottleneck for current parallel speculative decoding.

A natural solution to this bottleneck is tree drafting ([Miao et al., 2024](#bib.bib11); [Cai et al., 2024](#bib.bib10); [Li et al., 2024a](#bib.bib13)), which retains multiple draft paths as tree branches, increasing the chance that target verification matches one of them. By providing diverse yet plausible candidate drafts, tree drafting is more robust in high-entropy scenarios. Combining tree drafting and parallel drafters by constructing budgeted trees from pretrained block-parallel drafters achieves considerable speedups ([Ringel and Romano, 2026](#bib.bib19); [Li et al., 2026c](#bib.bib18)). Nevertheless, these methods exhibit two limitations. First, the tension between token-wise dependency and full parallelism constrains the tradeoff between draft quality and drafting latency. Existing tree-based methods use autoregressive heads to capture token-wise dependencies, which precludes full parallelization. Conversely, omitting token-wise dependency limits the acceptance length and, consequently, the end-to-end speedup. Second, tree-based parallel methods suffer from a train–inference mismatch: they directly apply parallel drafters trained for single-path drafting to multi-path tree verification. Such drafters are optimized to produce the top draft for single-path verification, but are suboptimal for proposing multiple plausible paths for tree verification. Consequently, although lower-ranked alternatives in the draft tree can populate additional branches, they are not sufficiently optimized to align with the target model’s alternatives or worth allocating verification budget to.

We address these limitations with UBTree, a tree-based drafter with a parallel bigram selector to model token-wise dependencies and tree-native training to close the train–inference gap. We incorporate two designs in UBTree:

* •

  Architecture. UBTree separates drafting into three complementary stages and keeps all neural computation parallel. First, we use DFlash ([Chen et al., 2026](#bib.bib5)) as a unigram proposer to independently generate candidate tokens for every position in a drafting block. Second, a redesigned bigram selector scores adjacent candidate-token pairs conditioned on the proposer hidden states. It derives predecessor and successor representations from frozen target embeddings through separate MLPs and learns depth-dependent weights for combining proposer logits and selector scores. Third, we use the resulting transition scores to construct the verification tree. By simplifying the token-wise dependency into bigram correlation, we overcome the challenge of parallelizing token-wise dependency in tree drafting.
* •

  Training. Unlike other drafters trained on target-regenerated rollouts at the inference temperature, we use a renormalized KL training objective on high-temperature regenerated target trajectories to diversify the positive training labels. This tree-native training strategy allocates more supervision signals to plausible alternative paths in the target distribution and distinguishes them better from low-quality alternative paths in tree construction, thereby relieving the train–inference mismatch in tree drafting.

We extensively evaluate UBTree on both academic and production-scale benchmarks. UBTree outperforms all existing methods on both academic-scale and production benchmarks. It achieves an average decoding speedup of 5.845.84–6.94×6.94\times over autoregressive decoding on Qwen3-4B and Qwen3-8B with increased acceptance lengths. It also rivals frontier baselines such as DSpark ([Cheng et al., 2026](#bib.bib16)) in the acceleration of production LLMs like Ling3-Flash-124B. Additionally, UBTree shows outstanding durability on long-context tasks compared to baselines. In summary, UBTree provides a frontier solution for accelerating LLMs in both academic settings and production environments.

## 2 Background

Speculative Decoding.
Given a verified prefix x≤tx\_{\leq t}, a lightweight draft model proposes γ\gamma future tokens, which the target model verifies in one forward pass ([Leviathan et al., 2023](#bib.bib8); [Chen et al., 2023](#bib.bib9)).
Each round accepts consecutive draft tokens from the start of the proposed block until the first rejection.
Let τ∈[1,γ+1]\tau\in[1,\gamma+1] denote the average of accepted tokens per round or acceptance length, including a token x0x\_{0} prefilled by the last verification.
With TdraftT\_{\mathrm{draft}} covering proposal construction and TverifyT\_{\mathrm{verify}} covering verification and commit work, the average per-token latency and speedup are ([Chen et al., 2026](#bib.bib5); [Huang et al., 2026](#bib.bib7))

|  |  |  |  |
| --- | --- | --- | --- |
|  | Lspec=Tdraft+Tverifyτ,η=LtargetLspec,L\_{\mathrm{spec}}=\frac{T\_{\mathrm{draft}}+T\_{\mathrm{verify}}}{\tau},\qquad\eta=\frac{L\_{\mathrm{target}}}{L\_{\mathrm{spec}}}, |  | (1) |

where LtargetL\_{\mathrm{target}} is the per-token latency of target-only autoregressive decoding.
DFlash & DFlash 2.
DFlash ([Chen et al., 2026](#bib.bib5)) proposes a γ\gamma-token block in parallel, conditioned on target hidden features through key-value context of one target prefilling forward. We denote the prefilled token x0x\_{0} by anchor token. For each future draft position i=1,…,γi=1,...,\gamma, one proposer forward pass produces final hidden state hih\_{i}, which is subsequently mapped to proposer logit uiu\_{i} through the frozen target LM head. The draft tokens of DFlash are predicted in parallel from masks where little token-wise dependencies are involved. DFlash 2 ([Inco AI, 2026](#bib.bib17)) fixes this by adding convolutions to the DFlash backbone and a low-rank bigram selector. For predecessor aa and successor bb at position ii, the selector score δi​(a,b)\delta\_{i}(a,b) is added to the proposer logit ui​(b)u\_{i}(b) to obtain a combined score:

|  |  |  |  |
| --- | --- | --- | --- |
|  | δi​(a,b)=(P⁡(hi)⊙ϕ⁡(a))⊤​ψ​(b),ui′​(a,b)=ui​(b)+δi​(a,b),\delta\_{i}(a,b)=\bigl(P(h\_{i})\odot\phi(a)\bigr)^{\top}\psi(b),\qquad u\_{i}^{\prime}(a,b)=u\_{i}(b)+\delta\_{i}(a,b), |  | (2) |

where ⊙\odot stands for Hadamard product. Here, the linear projector PP maps hih\_{i} to a low-dimensional space, and ϕ\phi and ψ\psi are low-rank embeddings for predecessor and successor tokens, respectively. The selector scores all adjacent pairs from the position-wise top-KK candidate sets in parallel; token selection then follows a single chain using the combined scores.

Tree Drafting.
DFlash and DFlash 2 are single-path drafting methods, which propose a single γ\gamma-token draft path to match a γ\gamma-token target path for the target model to verify. Tree drafting, by contrast, constructs a draft tree storing multiple candidate draft paths. Taking candidate tokens as nodes, different paths share nodes across continuations with common prefixes. We then use tree attention to verify the whole draft tree in one target-model pass and picks the path with the longest accepted token continuations by the target model in the tree ([Miao et al., 2024](#bib.bib11); [Cai et al., 2024](#bib.bib10)). This verification procedure maintains the lossless property of speculative decoding, and accepted path need not be the proposer’s top-ranked.

DDTree ([Ringel and Romano, 2026](#bib.bib19)) and DARTree ([Li et al., 2026c](#bib.bib18)) construct budgeted trees from block-parallel proposals. DDTree uses best-first search, ranking paths by accumulated position-wise token log-probabilities. DARTree corrects token log-probabilities by a lightweight autoregressive head and ranks the cumulative log-probabilities with a depth decay and a WW node budget at each depth. These retained nodes accumulate into a candidate supertree of maximum depth γ\gamma, from which the BB highest-scoring non-root nodes are selected for verification. Correction at the next depth still depends on the tokens selected at the preceding depth, leading to extra overheads.

![Refer to caption](2609.39972v1/ubtree_diagram.png)

Figure 2: Overview of UBTree. Left: UBTree Architecture. The unigram proposer generates top-KK candidates at each draft position in parallel. The bigram selector scores adjacent candidate transitions in parallel, and tree construction uses these precomputed scores to build a verification tree. Right: Tree-native Training. Our training combines high-temperature target traces with renormalized KL supervision to encourage plausible alternative branches.

## 3 Method

Two key designs of UBTree are 1) parallelizing token-wise dependency modeling in tree drafting and 2) training the tree drafter towards optimal tree drafting. Section [3.1](#S3.SS1 "3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") first explains how we incorporate token-dependencies with fully parallelized neural compuation in tree drafting. We use two parallel neural forwards to propose candidate tokens at each block position (Section [3.1.1](#S3.SS1.SSS1 "3.1.1 Unigram Proposer ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding")) and select transition paths among these candidates (Section [3.1.2](#S3.SS1.SSS2 "3.1.2 Bigram Selector ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding")). The verification tree is then built from paths selected by the selector (Section [3.1.3](#S3.SS1.SSS3 "3.1.3 Tree Construction and Verification ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding")). Section [3.2](#S3.SS2 "3.2 Tree-native Training ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") presents our tree-native training, which regenerates the target rollouts for training under high temperatures and trains the drafter with a renormalized KL objective. We summarize these two designs of UBTree in Figure [2](#S2.F2 "Figure 2 ‣ 2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").

### 3.1 UBTree Architecture

#### 3.1.1 Unigram Proposer

The unigram proposer is designed to propose candidate tokens at each position without considering cross-token dependencies. Let cc be the key-value context from verified prefixes and x0x\_{0} be the prefilled anchor token. The unigram proposer can be formalized by

|  |  |  |  |
| --- | --- | --- | --- |
|  | qi(xi∣x0,c)=softmax(ui(x0,c)),i=1,2,…,γ,q\_{i}(x\_{i}\mid x\_{0},c)=\operatorname{softmax}(u\_{i}(x\_{0},c)),\quad i=1,2,...,\gamma, |  | (3) |

where ii denotes the position in the block. Since the proposal at each position does not depend on each other, its neural forward could be easily parallelized. In practice, we deploy a pretrained DFlash backbone ([Chen et al., 2026](#bib.bib5)) as our unigram proposer, where its output logits are ui​(x0,c)u\_{i}(x\_{0},c) and probabilities are qi​(xi∣x0,c)q\_{i}(x\_{i}\mid x\_{0},c). We also denote its predicted hidden states by hih\_{i}. We do not use DFlash2 backbone ([Inco AI, 2026](#bib.bib17)) because it differs from DFlash backbone by strengthening token-wise connection, which is not the task of our unigram proposal.

Candidate Sets.
We pick the tokens with top-KK probabilities in qiq\_{i} at each position as candidate tokens of this position 𝒞i\mathcal{C}\_{i}, with 𝒞0={xt}\mathcal{C}\_{0}=\{x\_{t}\}. The Cartesian product 𝒞1×⋯×𝒞γ\mathcal{C}\_{1}\times\cdots\times\mathcal{C}\_{\gamma} forms KγK^{\gamma} candidate paths. Enumerating these paths is infeasible, so UBTree scores their adjacent transitions and searches a bounded subset by the bigram selector in the next section.

#### 3.1.2 Bigram Selector

Inspired by DFlash 2 ([Inco AI, 2026](#bib.bib17)), we incorporate a lightweight bigram selector scores adjacent predecessor–successor token pairs from candidates, conditioned on the proposer hidden state hih\_{i} at the successor position. This trainable selector models token-wise dependencies in a parallel manner. To improve the selector, we redesign its architecture with deep codebooks and depth calibration.

Deep Codebooks.
For predecessor token aa and successor candidate bb at position ii, DFlash 2 learns two vocabulary-wide codebooks ϕ\phi and ψ\psi by two embedding layers (See equation [2](#S2.E2 "In 2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding")). UBTree instead derives the codebooks from the frozen target token embedding ev∈ℝdee\_{v}\in\mathbb{R}^{d\_{e}} and two bias-free MLPs:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ϕ⁡(v)=Wϕ,2​SiLU⁡(Wϕ,1​ev),ψ⁡(v)=Wψ,2​SiLU⁡(Wψ,1​ev).\phi(v)=W\_{\phi,2}\,\operatorname{SiLU}(W\_{\phi,1}e\_{v}),\qquad\psi(v)=W\_{\psi,2}\,\operatorname{SiLU}(W\_{\psi,1}e\_{v}). |  | (4) |

At inference, we precompute both MLPs once and store them as a vocabulary-wide lookup table. While keeping inference efficiency, our deep codebook introduces nonlinearity and makes use of features in the target embedding. Hence, it improves the selector performance.

Depth Calibration.
DFlash 2 combines proposer logits and selector scores with fixed unit weights. However, their reliability can vary across draft depths. UBTree therefore learns two positive, depth-dependent scales:

|  |  |  |  |
| --- | --- | --- | --- |
|  | si​(a,b)=αi​ui​(b)+λi​δi​(a,b),αi=exp⁡(ρi),λi=exp⁡(κi).s\_{i}(a,b)=\alpha\_{i}u\_{i}(b)+\lambda\_{i}\delta\_{i}(a,b),\qquad\alpha\_{i}=\exp(\rho\_{i}),\quad\lambda\_{i}=\exp(\kappa\_{i}). |  | (5) |

The ratio λi/αi\lambda\_{i}/\alpha\_{i} controls the weight of selector scores relative to proposer logits, while their common magnitude controls the concentration of the normalized successor distribution. These scales depend only on depth and preserve parallel edge scoring.

Parallel Computation.
Once the proposer provides the candidate sets and hidden states, we compute transition scores for all K+(γ−1)​K2K+(\gamma-1)K^{2} predecessor-successor token pairs in parallel. At depth ii, let 𝚽i−1\bm{\Phi}\_{i-1} have rows ϕ​(a)⊤\phi(a)^{\top} for predecessor candidates a∈𝒞i−1a\in\mathcal{C}\_{i-1}, and let 𝚿i\bm{\Psi}\_{i} have rows ψ​(b)⊤\psi(b)^{\top} for successor candidates b∈𝒞ib\in\mathcal{C}\_{i}. With proposer’s hidden state hih\_{i} at the successor position, we obtain

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝚫i=𝚽i−1​diag⁡(P⁡(hi))​𝚿i⊤∈ℝ|𝒞i−1|×K.\bm{\Delta}\_{i}=\bm{\Phi}\_{i-1}\operatorname{diag}\!\bigl(P(h\_{i})\bigr)\bm{\Psi}\_{i}^{\top}\in\mathbb{R}^{|\mathcal{C}\_{i-1}|\times K}. |  | (6) |

Here, diag⁡(⋅)\operatorname{diag}(\cdot) places the input vector on the diagonal. The entry at the row for aa and column for bb is the selector score δi​(a,b)\delta\_{i}(a,b). After combining δi​(a,b)\delta\_{i}(a,b) with proposer logits ui​(b)u\_{i}(b) via equation [5](#S3.E5 "In 3.1.2 Bigram Selector ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"), tree construction can proceed depth by depth sequentially without any neural computation.

#### 3.1.3 Tree Construction and Verification

With unique scores for every transition si​(a,b)s\_{i}(a,b) in Ci−1×CiC\_{i-1}\times C\_{i}, we are able to score all KγK^{\gamma} candidate paths consisting of these transitions without neural computation. Specifically, we can normalize si​(a,b)s\_{i}(a,b) into log-probabilities over successor candidates, then rank paths by cumulative log-probabilities. However, to save the computation cost, we use DARTree’s depth-wise progressive tree construction and global pruning procedure ([Li et al., 2026c](#bib.bib18)) instead of traversing all possible paths. After tree construction, target model will verify the whole tree in one-forward pass via tree attention, and keep the longest accepted continuation for lossless acceleration. Appendix [A](#A1 "Appendix A Tree Construction Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") specifies the normalization, path scoring, search and verification procedure.

### 3.2 Tree-native Training

Tree drafting recommends multiple paths for target verification, rather than only proposing the greedy path. Hence, we need to diversify positive training signals to help the selector better recognize alternative plausible paths other than the greedy one. To this end, we use higher temperature TtrainT\_{\mathrm{train}} to regenerate the training data than the inference temperature TinferT\_{\mathrm{infer}} and supervise the training by a renormalized KL objective.

Training with Ttrain≥TinferT\_{\mathrm{train}}\geq T\_{\mathrm{infer}} for different TinferT\_{\mathrm{infer}}.
The training temperature TtrainT\_{\mathrm{train}} controls both the continuation distribution seen by the proposer and selector and the target distribution used for KL supervision. Temperature-matched training would set Ttrain=TinferT\_{\mathrm{train}}=T\_{\mathrm{infer}}. As mentioned above, the selector needs to improve the plausibility of multiple paths in the tree, rather than focusing only on the top path. We can therefore make Ttrain≥TinferT\_{\mathrm{train}}\geq T\_{\mathrm{infer}} to make those high-probability alternative paths more distinguishable. TtrainT\_{\mathrm{train}} then becomes an independent hyper-parameter to be tuned empirically. The best TtrainT\_{\mathrm{train}} amplifies the probability gap between plausible and other choices. Interestingly, TtrainT\_{\mathrm{train}} is disentangled with TinferT\_{\mathrm{infer}} to some extent, that one UBTree drafter trained on TtrainT\_{\mathrm{train}} can be used in different TinferT\_{\mathrm{infer}}, which simplifies the drafter adaptation. We therefore use drafters trained at Ttrain=1T\_{\mathrm{train}}=1 for both Tinfer=0T\_{\mathrm{infer}}=0 and Tinfer=1T\_{\mathrm{infer}}=1 in our experiments.

Renormalized KL Loss. To train the selector to better discriminate between alternates other than the top choice, we use the forward KL divergence between the renormalized probabilities ([Zhu et al., 2026](#bib.bib20)) of the target and that of the selector over the proposer’s top-KK candidate tokens instead of the classical cross-entropy (CE) loss. For each valid future position, let zi​(v)z\_{i}(v) be the target logit and si​(yi−1∗,v)s\_{i}(y\_{i-1}^{\*},v) be the selector logit given the predecessor token yi−1∗y\_{i-1}^{\*}. For Ttrain>0T\_{\mathrm{train}}>0, we define the renormalized target probabilities p~i​(v)\widetilde{p}\_{i}(v) at training temperature TtrainT\_{\mathrm{train}} and the selector probabilities q~i​(v)\widetilde{q}\_{i}(v) on the top-KK token support 𝒞i\mathcal{C}\_{i}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | p~i​(v)=exp⁡(zi​(v)/Ttrain)∑b∈𝒞iexp⁡(zi​(b)/Ttrain),q~i​(v)=exp⁡(si​(yi−1∗,v))∑b∈𝒞iexp⁡(si​(yi−1∗,b)).\widetilde{p}\_{i}(v)=\frac{\exp(z\_{i}(v)/T\_{\mathrm{train}})}{\sum\_{b\in\mathcal{C}\_{i}}\exp(z\_{i}(b)/T\_{\mathrm{train}})},\qquad\widetilde{q}\_{i}(v)=\frac{\exp(s\_{i}(y\_{i-1}^{\*},v))}{\sum\_{b\in\mathcal{C}\_{i}}\exp(s\_{i}(y\_{i-1}^{\*},b))}. |  | (7) |

For Ttrain=0T\_{\mathrm{train}}=0, the target distribution is understood in the limit Ttrain→0+T\_{\mathrm{train}}\to 0^{+}.
The forward KL divergence between p~i​(v)\widetilde{p}\_{i}(v) and q~i​(v)\widetilde{q}\_{i}(v) constitutes the main term of our training objective. An auxiliary cross-entropy term, also used in the first-stage proposer training, is applied solely to the proposer qiq\_{i} to maintain the candidate distribution. Using weight β\beta to balance two terms, the joint objective is

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒ=KL⁡(p~i|q~i)−β​log⁡qi​(yi∗∣x≤t),β=0.1.\mathcal{L}=\mathrm{KL}(\widetilde{p}\_{i}|\widetilde{q}\_{i})-\beta\log q\_{i}(y\_{i}^{\*}\mid x\_{\leq t}),\qquad\beta=0.1. |  | (8) |

## 4 Experiments

We evaluate UBTree on benchmarks and report decoding speedup η\eta over autoregressive baseline and average acceptance length τ\tau. Avg. means average results across all listed benchmarks.

Table 1: Speedup and average acceptance length (τ\tau) on instruct and reasoning models. All τ\tau values include the target-produced bonus token. M-500, HE, LCB, and MT-B denote MATH-500, HumanEval, LiveCodeBench, and MT-Bench. †\dagger values are paper-reported.

| Instruct Models | | | | | | | | | | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model | Method | Math | | | | | | Code | | | | | | Chat | |  | |
| GSM8K | | M-500 | | AIME | | HE | | MBPP | | LCB | | MT-B | | Avg. | |
| Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau |
| Qwen3-4B Tinfer=0T\_{\mathrm{infer}}=0 | Single-path | | | | | | | | | | | | | | | | |
| DFlash (16) | 5.95 | 8.57 | 5.76 | 8.34 | 4.45 | 6.34 | 4.28 | 6.08 | 4.03 | 5.82 | 3.83 | 5.39 | 2.69 | 4.60 | 4.43 | 6.45 |
| Domino†\dagger (17) | 8.02 | 10.12 | 7.14 | 9.01 | 5.97 | 7.49 | 5.66 | 7.02 | 5.59 | 7.11 | 5.33 | 6.86 | 3.28 | 5.12 | 5.86 | 7.53 |
| Tree-based | | | | | | | | | | | | | | | | |
| EAGLE-3 (16) | 4.04 | 7.20 | 3.97 | 6.96 | 3.45 | 6.05 | 3.46 | 6.07 | 3.42 | 6.05 | 3.19 | 5.53 | 2.40 | 4.67 | 3.42 | 6.08 |
| EAGLE-3 (64) | 4.42 | 7.97 | 4.45 | 7.85 | 4.02 | 7.11 | 4.00 | 7.07 | 3.95 | 7.11 | 3.75 | 6.58 | 2.80 | 5.46 | 3.91 | 7.02 |
| DDTree (64) | 6.69 | 10.22 | 6.62 | 10.10 | 5.51 | 8.49 | 5.18 | 7.89 | 5.10 | 7.80 | 4.78 | 7.23 | 3.51 | 6.14 | 5.34 | 8.27 |
| DARTree (64) | 7.89 | 12.50 | 7.63 | 11.90 | 6.55 | 10.37 | 6.09 | 9.78 | 6.33 | 10.07 | 5.75 | 9.04 | 3.93 | 7.23 | 6.31 | 10.13 |
| UBTree (64) | 8.54 | 12.58 | 8.18 | 12.15 | 6.92 | 10.13 | 7.07 | 10.22 | 6.66 | 9.98 | 6.37 | 9.24 | 4.39 | 7.32 | 6.88 | 10.23 |
| Qwen3-4B Tinfer=1T\_{\mathrm{infer}}=1 | Single-path | | | | | | | | | | | | | | | | |
| DFlash (16) | 5.28 | 7.67 | 4.56 | 6.89 | 3.10 | 4.64 | 4.09 | 5.86 | 3.84 | 5.52 | 3.25 | 4.62 | 2.52 | 4.26 | 3.81 | 5.64 |
| Domino†\dagger (17) | 6.79 | 8.61 | 5.67 | 7.35 | 3.75 | 4.83 | 5.02 | 6.30 | 4.96 | 6.36 | 5.04 | 6.45 | 3.02 | 4.56 | 4.89 | 6.35 |
| Tree-based | | | | | | | | | | | | | | | | |
| EAGLE-3 (16) | 3.66 | 6.61 | 3.51 | 6.36 | 2.72 | 4.88 | 3.34 | 5.93 | 3.21 | 5.80 | 2.80 | 4.94 | 2.21 | 4.34 | 3.06 | 5.55 |
| EAGLE-3 (64) | 4.13 | 7.66 | 3.96 | 7.29 | 3.20 | 6.00 | 3.75 | 6.84 | 3.71 | 6.92 | 3.27 | 5.96 | 2.54 | 5.12 | 3.51 | 6.54 |
| DDTree (64) | 6.19 | 9.49 | 5.62 | 8.76 | 4.14 | 6.31 | 5.17 | 7.81 | 4.90 | 7.50 | 4.19 | 6.37 | 3.37 | 5.66 | 4.80 | 7.41 |
| DARTree (64) | 6.94 | 11.01 | 6.05 | 9.73 | 4.10 | 6.99 | 5.84 | 9.10 | 5.76 | 9.28 | 4.71 | 7.33 | 3.64 | 6.53 | 5.29 | 8.57 |
| UBTree (64) | 7.95 | 11.79 | 7.13 | 10.54 | 5.10 | 7.63 | 6.42 | 9.43 | 6.15 | 9.30 | 5.27 | 7.72 | 4.02 | 6.68 | 6.00 | 9.01 |
| Qwen3-8B Tinfer=0T\_{\mathrm{infer}}=0 | Single-path | | | | | | | | | | | | | | | | |
| DFlash (16) | 5.98 | 8.59 | 5.84 | 8.51 | 4.75 | 6.73 | 4.46 | 6.31 | 4.07 | 5.87 | 3.91 | 5.48 | 2.64 | 4.54 | 4.52 | 6.58 |
| Domino†\dagger (17) | 7.92 | 10.03 | 7.38 | 9.43 | 5.85 | 7.41 | 5.89 | 7.39 | 5.53 | 7.04 | 5.27 | 7.04 | 3.29 | 5.18 | 5.88 | 7.65 |
| Tree-based | | | | | | | | | | | | | | | | |
| EAGLE-3 (16) | 4.23 | 7.43 | 4.20 | 7.30 | 3.71 | 6.46 | 3.68 | 6.42 | 3.62 | 6.39 | 3.54 | 6.07 | 2.53 | 4.88 | 3.64 | 6.42 |
| EAGLE-3 (64) | 4.57 | 8.20 | 4.66 | 8.11 | 4.34 | 7.51 | 4.23 | 7.39 | 4.13 | 7.39 | 4.11 | 7.10 | 2.99 | 5.77 | 4.15 | 7.35 |
| DDTree (64) | 6.65 | 10.19 | 6.60 | 10.12 | 5.64 | 8.63 | 5.43 | 8.17 | 5.07 | 7.68 | 4.92 | 7.30 | 3.49 | 6.09 | 5.40 | 8.31 |
| DARTree (64) | 8.26 | 12.49 | 7.61 | 12.13 | 6.71 | 10.37 | 6.41 | 10.09 | 6.32 | 10.02 | 5.88 | 9.19 | 4.01 | 7.33 | 6.46 | 10.23 |
| UBTree (64) | 8.65 | 12.58 | 8.46 | 12.30 | 7.05 | 10.17 | 7.12 | 10.12 | 6.64 | 9.79 | 6.43 | 9.24 | 4.25 | 7.25 | 6.94 | 10.21 |
| Qwen3-8B Tinfer=1T\_{\mathrm{infer}}=1 | Single-path | | | | | | | | | | | | | | | | |
| DFlash (16) | 5.05 | 7.37 | 4.57 | 6.77 | 2.99 | 4.47 | 3.74 | 5.26 | 3.64 | 5.20 | 3.14 | 4.41 | 2.34 | 3.96 | 3.64 | 5.35 |
| Domino†\dagger (17) | 6.47 | 8.34 | 5.40 | 7.20 | 3.78 | 4.92 | 4.75 | 5.98 | 4.73 | 6.02 | 5.06 | 6.72 | 2.94 | 4.61 | 4.73 | 6.26 |
| Tree-based | | | | | | | | | | | | | | | | |
| EAGLE-3 (16) | 3.93 | 7.07 | 3.74 | 6.68 | 3.01 | 5.30 | 3.35 | 5.89 | 3.35 | 6.01 | 3.01 | 5.25 | 2.36 | 4.55 | 3.25 | 5.82 |
| EAGLE-3 (64) | 4.39 | 8.05 | 4.23 | 7.65 | 3.51 | 6.34 | 3.88 | 7.00 | 3.88 | 7.14 | 3.53 | 6.32 | 2.73 | 5.45 | 3.73 | 6.85 |
| DDTree (64) | 6.10 | 9.23 | 5.61 | 8.68 | 4.04 | 6.31 | 4.91 | 7.37 | 4.63 | 7.02 | 4.14 | 6.22 | 3.23 | 5.48 | 4.67 | 7.19 |
| DARTree (64) | 7.04 | 11.01 | 5.86 | 9.59 | 4.48 | 7.21 | 5.26 | 8.36 | 5.53 | 8.91 | 4.45 | 7.06 | 3.59 | 6.48 | 5.17 | 8.37 |
| UBTree (64) | 7.97 | 11.55 | 6.99 | 10.44 | 4.99 | 7.43 | 6.17 | 8.85 | 5.92 | 8.80 | 5.10 | 7.47 | 3.77 | 6.36 | 5.84 | 8.70 |

| Reasoning Models | | | | | | | | | | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model | Method | Math | | | | | | Code | | | | | | Chat | |  | |
| GSM8K | | M-500 | | AIME | | HE | | MBPP | | LCB | | MT-B | | Avg. | |
| Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau |
| Qwen3-4B Tinfer=0T\_{\mathrm{infer}}=0 | Single-path | | | | | | | | | | | | | | | | |
| DFlash (16) | 5.18 | 7.28 | 4.53 | 6.45 | 3.67 | 5.26 | 3.91 | 5.46 | 3.72 | 5.17 | 3.37 | 4.68 | 2.99 | 4.64 | 3.91 | 5.56 |
| Tree-based | | | | | | | | | | | | | | | | |
| EAGLE-3 (16) | 3.49 | 6.01 | 3.04 | 5.23 | 2.65 | 4.62 | 2.82 | 4.83 | 2.80 | 4.78 | 2.43 | 4.16 | 2.25 | 4.11 | 2.78 | 4.82 |
| EAGLE-3 (64) | 4.19 | 7.24 | 3.75 | 6.48 | 3.29 | 5.77 | 3.52 | 6.05 | 3.51 | 6.04 | 3.04 | 5.28 | 2.74 | 5.07 | 3.44 | 5.99 |
| DDTree (64) | 6.09 | 9.19 | 5.54 | 8.42 | 4.77 | 7.20 | 4.85 | 7.29 | 4.68 | 7.01 | 4.31 | 6.45 | 3.82 | 6.15 | 4.87 | 7.39 |
| UBTree (64) | 7.64 | 10.95 | 6.99 | 10.01 | 5.73 | 8.53 | 6.21 | 8.85 | 5.98 | 8.54 | 5.45 | 7.75 | 4.71 | 7.22 | 6.10 | 8.84 |
| Qwen3-4B Tinfer=1T\_{\mathrm{infer}}=1 | Single-path | | | | | | | | | | | | | | | | |
| DFlash (16) | 4.80 | 6.77 | 4.36 | 6.18 | 3.57 | 5.15 | 3.76 | 5.23 | 3.55 | 4.93 | 3.21 | 4.47 | 2.89 | 4.40 | 3.73 | 5.30 |
| Tree-based | | | | | | | | | | | | | | | | |
| EAGLE-3 (16) | 3.01 | 5.28 | 2.78 | 4.86 | 2.41 | 4.22 | 2.54 | 4.42 | 2.47 | 4.28 | 2.24 | 3.92 | 2.00 | 3.69 | 2.49 | 4.38 |
| EAGLE-3 (64) | 3.64 | 6.57 | 3.34 | 6.00 | 2.98 | 5.37 | 3.17 | 5.66 | 3.06 | 5.48 | 2.77 | 4.99 | 2.35 | 4.49 | 3.04 | 5.51 |
| DDTree (64) | 4.87 | 7.35 | 4.69 | 7.11 | 4.01 | 6.10 | 4.17 | 6.22 | 3.97 | 5.93 | 3.57 | 5.37 | 3.28 | 5.11 | 4.08 | 6.17 |
| UBTree (64) | 6.56 | 9.50 | 6.12 | 8.78 | 5.12 | 7.47 | 5.44 | 7.74 | 5.18 | 7.41 | 4.57 | 6.61 | 4.10 | 6.17 | 5.30 | 7.67 |

### 4.1 Academic-scale Experiment

Benchmarks.
We evaluate UBTree on Qwen3-4B and Qwen3-8B ([Yang et al., 2025a](#bib.bib49)) with thinking disabled (instruct models), and on Qwen3-4B with thinking enabled (reasoning models), under Tinfer={0,1}T\_{\mathrm{infer}}=\{0,1\}. The benchmarks cover math (GSM8K ([Cobbe et al., 2021](#bib.bib21)), MATH-500 ([Lightman et al., 2024](#bib.bib22)), and AIME), code (HumanEval ([Chen et al., 2021](#bib.bib23)), MBPP ([Austin et al., 2021](#bib.bib24)), and LiveCodeBench ([Jain et al., 2025](#bib.bib25))), and dialogue (MT-Bench ([Zheng et al., 2023](#bib.bib26))).

Implementation.
We train UBTree on OpenPerfectBlend ([Xu et al., 2024](#bib.bib29)) with regenerated target responses under Ttrain=1T\_{\mathrm{train}}=1. We retrain DFlash ([Chen et al., 2026](#bib.bib5)) proposer with block size 16 with SpecForge ([Li et al., 2026b](#bib.bib30)) for 6 epochs till convergence, and then jointly train the proposer and selector for 2 epochs, with selector and backbone learning rates of 6×10−46\times 10^{-4} and 2×10−52\times 10^{-5}, respectively. Unlike baselines that need different checkpoints for different decoding temperatures TinferT\_{\mathrm{infer}}, we use the same checkpoint of UBTree trained under Ttrain=1T\_{\mathrm{train}}=1 is used at Tinfer={0,1}T\_{\mathrm{infer}}=\{0,1\}. Our evaluations use 1×1\timesNVIDIA H200 with batch size 1 and the transformers backend. For tree construction, we follow DARTree ([Li et al., 2026c](#bib.bib18)) with B=64B=64 non-root nodes, a search width of W=12W=12, and K=64K=64 candidate tokens per position, but use a different depth bonus of ζ=0\zeta=0. Training and evaluation protocols are detailed in Appendix [B](#A2 "Appendix B Experimental Setup Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").

Baselines.
We compare UBTree with single-path methods DFlash ([Chen et al., 2026](#bib.bib5)) and Domino ([Huang et al., 2026](#bib.bib7)), and tree-based EAGLE-3 ([Li et al., 2026d](#bib.bib6)), DDTree ([Ringel and Romano, 2026](#bib.bib19)), and DARTree ([Li et al., 2026c](#bib.bib18)), with budgets in Table [1](#S4.T1 "Table 1 ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"). We retrain EAGLE-3 and DFlash on the same OpenPerfectBlend dataset for 6 epochs at corresponding TinferT\_{\mathrm{infer}} and report Domino results (with block size 17) from its original paper, trained on OpenPerfectBlend as well. We re-evaluate DDTree and DARTree using retrained DFlash and released Domino checkpoints, respectively, under their original setups. Due to lack of released checkpoints, Domino and DARTree are compared only for instruct models. For fair comparison, we cap the maximum draft depth of DARTree at 16 to match DDTree and UBTree, since the underlying Domino checkpoint uses a block size of 17 and would otherwise permit a larger maximum acceptance length.

Results.
Table [1](#S4.T1 "Table 1 ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") shows that UBTree achieves average speedups of 6.88×6.88\times and 6.94×6.94\times on Qwen3-4B and Qwen3-8B under greedy decoding, and 6.00×6.00\times and 5.84×5.84\times under temperature-1 sampling. It outperforms DARTree over all 28 benchmarks in speedups, improving the average by 7.47.4–13.4%13.4\%. With thinking enabled on Qwen3-4B, UBTree outperforms DDTree by 25.3%25.3\% and 29.9%29.9\% in average speedup at Tinfer=0T\_{\mathrm{infer}}=0 and 11, respectively. Our superiority especially stands out under Tinfer=1T\_{\mathrm{infer}}=1, validating the effectiveness of our high entropy adaptions.

Concurrent Serving.
Table [2](#S4.T2 "Table 2 ‣ 4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") compares UBTree and baselines in SGLang ([Zheng et al., 2024](#bib.bib31)) at client concurrency C∈{1,8,16,32}C\in\{1,8,16,32\}. All methods use SGLang in BF16 on one NVIDIA H200 with CUDA Graphs. Results are aggregated from the same benchmarks as in Section [4.1](#S4.SS1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"). Following DARTree ([Li et al., 2026c](#bib.bib18)), we employ an adaptive-tree strategy that selects different tree budget BB and width WW according to the serving load. We tune B/WB/W separately for each method and concurrency using the same candidate configuration set and selection criterion. At C∈{1,8,16,32}C\in\{1,8,16,32\}, UBTree uses B/W=64/12,64/12,64/12,16/3B/W=64/12,64/12,64/12,16/3 for Qwen3-4B and B/W=64/12,64/12,16/12,16/3B/W=64/12,64/12,16/12,16/3 for Qwen3-8B and DARTree uses B/W=64/12,64/12,32/8,16/3B/W=64/12,64/12,32/8,16/3 on both models. UBTree achieves the highest throughput in all settings, outperforming the next-best method by 7.07.0–16.3%16.3\%. At C=32C=32, UBTree reaches 6560.4 and 5851.4 tokens/s on Qwen3-4B and Qwen3-8B, respectively, exceeding the strongest single-path baseline by 7.3%7.3\% and 7.7%7.7\%.

Table 2: Concurrent-serving results on Qwen3-4B and Qwen3-8B under Tinfer=1T\_{\mathrm{infer}}=1. Each cell reports aggregate output tokens/s / speedup over the AR baseline row at the same concurrency.

| Model | Method | C=1C=1 | C=8C=8 | C=16C=16 | C=32C=32 |
| --- | --- | --- | --- | --- | --- |
| Qwen3-4B | Autoregressive baseline | 253.5 / 1.00×1.00\times | 1404.9 / 1.00×1.00\times | 2208.3 / 1.00×1.00\times | 3307.4 / 1.00×1.00\times |
| DFlash | 796.4 / 3.14×3.14\times | 2287.2 / 1.63×1.63\times | 3664.4 / 1.66×1.66\times | 6071.9 / 1.84×1.84\times |
| Domino | 816.3 / 3.22×3.22\times | 2258.9 / 1.61×1.61\times | 3636.5 / 1.65×1.65\times | 6115.5 / 1.85×1.85\times |
| DDTree | 844.6 / 3.33×3.33\times | 2390.8 / 1.70×1.70\times | 3669.8 / 1.66×1.66\times | 4810.4 / 1.45×1.45\times |
| DARTree (adaptive B/WB/W) | 978.5 / 3.86×3.86\times | 2405.1 / 1.71×1.71\times | 3770.3 / 1.71×1.71\times | 5619.9 / 1.70×1.70\times |
| UBTree (adaptive B/WB/W) | 1089.1 / 4.30×4.30\times | 2797.4 / 1.99×1.99\times | 4271.9 / 1.93×1.93\times | 6560.4 / 1.98×1.98\times |
| Qwen3-8B | Autoregressive baseline | 180.9 / 1.00×1.00\times | 1126.2 / 1.00×1.00\times | 1865.9 / 1.00×1.00\times | 2770.9 / 1.00×1.00\times |
| DFlash | 634.7 / 3.51×3.51\times | 2181.7 / 1.94×1.94\times | 3596.0 / 1.93×1.93\times | 5265.4 / 1.90×1.90\times |
| Domino | 676.2 / 3.74×3.74\times | 2137.9 / 1.90×1.90\times | 3582.7 / 1.92×1.92\times | 5435.2 / 1.96×1.96\times |
| DDTree | 686.8 / 3.80×3.80\times | 2013.9 / 1.79×1.79\times | 3303.5 / 1.77×1.77\times | 3603.6 / 1.30×1.30\times |
| DARTree (adaptive B/WB/W) | 824.4 / 4.56×4.56\times | 2280.1 / 2.02×2.02\times | 3514.5 / 1.88×1.88\times | 4844.9 / 1.75×1.75\times |
| UBTree (adaptive B/WB/W) | 881.7 / 4.87×4.87\times | 2644.4 / 2.35×2.35\times | 4069.9 / 2.18×2.18\times | 5851.4 / 2.11×2.11\times |

Table 3: Speedup and acceptance length (τ\tau) on production-scale models. Each benchmark reports speedup and average acceptance length, and the Avg. columns are means over all benchmarks. M-500, HE, LCB, and MT-B denote MATH-500, HumanEval, LiveCodeBench, and MT-Bench.

| Model | Method | Math | | | | | | Code | | | | | | Chat | |  | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSM8K | | M-500 | | AIME | | HE | | MBPP | | LCB | | MT-B | | Avg. | |
| Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau |
| Ling3-Flash | DSpark | 5.14 | 6.09 | 4.93 | 5.81 | 4.22 | 4.96 | 5.37 | 6.32 | 4.50 | 5.93 | 4.18 | 4.98 | 3.19 | 3.74 | 4.50 | 5.40 |
| DFlash | 4.85 | 5.73 | 4.83 | 5.58 | 4.17 | 4.80 | 5.11 | 6.00 | 4.39 | 5.55 | 3.97 | 4.63 | 3.11 | 3.58 | 4.35 | 5.12 |
| UBTree | 5.83 | 7.37 | 5.87 | 7.18 | 5.43 | 6.60 | 5.94 | 7.42 | 5.00 | 6.85 | 5.22 | 6.54 | 4.24 | 5.27 | 5.36 | 6.75 |
| Qwen3.8-27B | DSpark | 5.20 | 6.74 | 4.76 | 6.07 | 4.41 | 5.65 | 5.18 | 6.85 | 4.26 | 5.79 | 3.47 | 4.53 | 3.00 | 3.82 | 4.32 | 5.64 |
| DFlash 2 | 4.65 | 6.29 | 4.67 | 6.29 | 4.48 | 6.00 | 5.06 | 6.98 | 4.30 | 6.11 | 3.55 | 4.82 | 2.92 | 3.95 | 4.24 | 5.78 |
| UBTree | 5.05 | 7.59 | 5.28 | 7.50 | 5.07 | 7.33 | 5.14 | 7.66 | 4.67 | 7.32 | 4.44 | 6.54 | 3.84 | 5.61 | 4.78 | 7.08 |

### 4.2 Production-scale Experiment

Evaluation.
We evaluate UBTree on two production models: Ling3-Flash (124B-A5.1B MoE) and Qwen3.8-27B ([Qwen Team, 2026](#bib.bib48)), on the same benchmarks as in Section [4.1](#S4.SS1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"). We compare UBTree with DSpark ([Cheng et al., 2026](#bib.bib16)) and DFlash ([Chen et al., 2026](#bib.bib5)) on the Ling3-Flash, and with DSpark and DFlash 2 ([Inco AI, 2026](#bib.bib17)) on Qwen3.8-27B. We construct target-specific training sets by regenerating responses with each target under thinking-disabled decoding. For baseline and UBTree training, Qwen3.8-27B uses OpenPerfectBlend ([Xu et al., 2024](#bib.bib29)) prompts, whereas Ling3-Flash uses supervised-finetuning corpus with 2.5M samples and 15B tokens under 64K context length. For Qwen3.8-27B, we load the officially released Qwen3.8-27B DFlash 2 checkpoint and fine-tune both DFlash 2 selector and UBTree selector for 2 epochs with a learning rate of 3×10−43\times 10^{-4} on our regenerated Qwen3.8-27B rollouts. For Ling3-Flash, we train DFlash with block size 8 for 3 epochs with the learning rate 2×10−52\times 10^{-5}. UBTree is then trained based on DFlash for 2 epochs with a learning rate of 3×10−43\times 10^{-4}. Our tree verification uses the setup in Section [4.1](#S4.SS1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").

SGLang Integration.
We implement UBTree in SGLang ([Zheng et al., 2024](#bib.bib31)). DFlash and DSpark use SGLang’s official implementation, while the Qwen3.8-27B implementations follow the official DFlash 2 codebase. We use TP degree 4 on four H200 GPUs, with the same degree for the target and draft models. All experiments use batch size 1 and greedy drafter decoding with thinking disabled. Ling3-Flash and Qwen3.8-27B use hybrid attention with Kimi Delta Attention ([Kimi Team et al., 2025](#bib.bib32)) and Gated DeltaNet ([Yang et al., 2025b](#bib.bib33)) layers, respectively. Inspired by Bole ([Wang et al., 2026a](#bib.bib36)), each node inherits recurrent and convolution states from its parent in tree verification, and only the states and KV entries on the accepted path are committed.

Results.
Table [3](#S4.T3 "Table 3 ‣ 4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") shows that UBTree achieves the highest acceptance length in all 14 model–benchmark comparisons and the highest speedup in 12 of them. Averaged over the seven benchmarks, UBTree reaches 5.36×5.36\times and 4.78×4.78\times speedup on Ling3-Flash and Qwen3.8-27B, respectively.

### 4.3 Long-context Tasks

Setup.
We evaluate acceptance length on Ling3-Flash using LongBench-v2 ([Bai et al., 2025](#bib.bib34)) for long inputs and SWE-bench ([Jimenez et al., 2024](#bib.bib35)) for long-continuation agentic tasks. For SWE-bench, all methods replay identical records. Evaluation Protocols are detailed in Appendix [B.3](#A2.SS3 "B.3 Long-context Evaluation Protocol ‣ Appendix B Experimental Setup Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").

Results.
Figure [1](#S0.F1 "Figure 1 ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") (c) shows that UBTree achieves the highest acceptance length in every context-length bin, exceeding the strongest baseline by 34.634.6–42.1%42.1\% on LongBench-v2 and 29.029.0–37.8%37.8\% on SWE-bench. These results show that UBTree retains its advantage under both long initial prompts and growing agent histories. Quantitative results are available in Appendix [C.2](#A3.SS2 "C.2 Long-context Tasks ‣ Appendix C Additional Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").

Table 4: 
Selector, training-temperature, and training-objective ablations on Qwen3-4B
with thinking disabled.
Top: speedup and acceptance length (τ\tau) at
Tinfer=0T\_{\mathrm{infer}}=0.
Middle: acceptance length across training and inference temperatures,
with the same checkpoints evaluated in both panels.
Bottom: training-objective ablation with the fixed architecture and training temperature.

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Math | | | | | | Code | | | | | | Chat | |  | |
|  | GSM8K | | M-500 | | AIME | | HE | | MBPP | | LCB | | MT-B | | Avg. | |
|  | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau | Speedup | τ\tau |
| DFlash 2 selector++Tree | 7.58 | 11.08 | 7.42 | 10.87 | 6.13 | 8.98 | 5.88 | 8.48 | 5.64 | 8.44 | 5.40 | 7.77 | 3.60 | 6.15 | 5.95 | 8.82 |
| UBTree selector++Tree | 8.16 | 12.11 | 7.83 | 11.67 | 6.79 | 10.06 | 6.73 | 9.61 | 6.21 | 9.54 | 6.04 | 8.78 | 4.26 | 7.23 | 6.57 | 9.86 |
| ++Ttrain=1T\_{\mathrm{train}}=1 | 8.54 | 12.58 | 8.18 | 12.15 | 6.92 | 10.13 | 7.07 | 10.22 | 6.66 | 9.98 | 6.37 | 9.24 | 4.39 | 7.32 | 6.88 | 10.23 |

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TtrainT\_{\mathrm{train}} | Tinfer=0T\_{\mathrm{infer}}=0: Acceptance length (τ\tau) | | | | | | | | Tinfer=1T\_{\mathrm{infer}}=1: Acceptance length (τ\tau) | | | | | | | |
| Math | | | Code | | | Chat |  | Math | | | Code | | | Chat |  |
| GSM8K | M-500 | AIME | HE | MBPP | LCB | MT-B | Avg. | GSM8K | M-500 | AIME | HE | MBPP | LCB | MT-B | Avg. |
| 0.8 | 12.58 | 12.12 | 10.57 | 10.00 | 9.82 | 9.15 | 7.26 | 10.21 | 11.72 | 10.47 | 7.52 | 9.39 | 9.17 | 7.63 | 6.58 | 8.93 |
| 1.0 | 12.58 | 12.15 | 10.13 | 10.22 | 9.98 | 9.24 | 7.32 | 10.23 | 11.79 | 10.54 | 7.63 | 9.43 | 9.30 | 7.72 | 6.68 | 9.01 |
| 1.1 | 12.64 | 12.04 | 10.08 | 10.09 | 9.77 | 9.02 | 7.15 | 10.11 | 11.71 | 10.52 | 7.61 | 9.48 | 9.12 | 7.71 | 6.69 | 8.98 |
| 1.2 | 12.59 | 11.94 | 9.90 | 10.10 | 9.87 | 9.01 | 7.22 | 10.09 | 11.72 | 10.61 | 7.47 | 9.31 | 9.40 | 7.80 | 6.72 | 9.00 |

| TinferT\_{\mathrm{infer}} | Selector loss | β\beta | Speedup | τ\tau | TinferT\_{\mathrm{infer}} | Selector loss | β\beta | Speedup | τ\tau |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Hard-label CE | 0.1 | 6.84 | 10.08 | 1 | Hard-label CE | 0.1 | 5.99 | 8.93 |
| 0 | Forward KL | 0.1 | 6.88 | 10.23 | 1 | Forward KL | 0.1 | 6.00 | 9.01 |
| 0 | Forward KL | 0 | 6.87 | 10.14 | 1 | Forward KL | 0 | 6.01 | 9.01 |

### 4.4 Ablation Studies

Architecture & High-temperature Training. We first ablate our two designs, selector architecture and high-temperature training temperature, on Qwen3-4B under Tinfer=0T\_{\mathrm{infer}}=0 and setups in Section [4.1](#S4.SS1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"). As shown in Table [4](#S4.T4 "Table 4 ‣ 4.3 Long-context Tasks ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") (Top), our selector architecture, combining deep codebooks and depth calibration, improves both speedup and acceptance length across all benchmarks, increasing their averages from 5.95×5.95\times to 6.57×6.57\times and from 8.828.82 to 9.869.86. A higher training temperature further helps reach an average speedup of 6.88×6.88\times and acceptance length of 10.2310.23, validating our tree-native training.

Training Temperature Sweeping. We then examine the optimal training temperature Tt​r​a​i​nT\_{train} of UBTree on Qwen3-4B by varying Ttrain∈{0.8,1.0,1.1,1.2}T\_{\mathrm{train}}\in\{0.8,1.0,1.1,1.2\} and evaluating each checkpoint at Tinfer∈{0,1}T\_{\mathrm{infer}}\in\{0,1\} in Table [4](#S4.T4 "Table 4 ‣ 4.3 Long-context Tasks ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") (Middle). Among the tested temperatures, Ttrain=1T\_{\mathrm{train}}=1 achieves the highest average acceptance length at both inference temperatures.

Training Objectives. We also compare different choices of training objectives by the average speedup and acceptance length over seven benchmarks in Table [4](#S4.T4 "Table 4 ‣ 4.3 Long-context Tasks ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") (Bottom). Both using the cross-entropy (CE) loss for the selector and disabling the CE loss for the proposer degrade the acceptance length at two inference temperatures. Additional ablation details are provided in Appendix [B.4](#A2.SS4 "B.4 Ablation Protocol ‣ Appendix B Experimental Setup Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").

## 5 Related Work

Parallel Drafting and Token-wise Dependencies.
DFlash generates tokens in a draft block in parallel ([Chen et al., 2026](#bib.bib5)). Domino and DSpark restore token-wise dependencies through sequential correction ([Huang et al., 2026](#bib.bib7); [Cheng et al., 2026](#bib.bib16)), whereas DFlash 2 uses a low-rank selector to score adjacent candidate pairs in parallel for single-path drafting ([Inco AI, 2026](#bib.bib17)). UBTree retains this scoring formulation but redesigns the token representations and learns depth-dependent weights for combining proposer logits and selector scores in tree verification.

Tree-based Speculative Decoding.
SpecInfer and Medusa retain multiple draft paths for tree verification ([Miao et al., 2024](#bib.bib11); [Cai et al., 2024](#bib.bib10)), while EAGLE-2 adapts tree structure to proposal confidence ([Li et al., 2024a](#bib.bib13)). DART applies nn-gram-guided pruning to parallel predictions ([Liu et al., 2026](#bib.bib15)). DDTree and DARTree construct trees from block-parallel proposals using position-wise probabilities and path-conditioned correction, respectively ([Ringel and Romano, 2026](#bib.bib19); [Li et al., 2026c](#bib.bib18)). Compared to existing tree drafting methods, UBTree exploits tree-native training to supervise the selector with target probabilities over alternatives rather than individual sampled tokens.

## 6 Conclusion

UBTree offers a new perspective on speculative decoding: tree verification calls for designs that explicitly account for multiple plausible generation paths. Its strong performance across benchmarks demonstrates the effectiveness of this principle. We also discuss limitations of our work in Appendix [D](#A4 "Appendix D Limitations ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"). Future work could further advance inference-time tree size selection, adapting the verification budget to balance candidate coverage and verification cost across different hardware, serving loads, and latency requirements.

## References

* An et al. (2026)
  Z. An, H. Bai, Z. Liu, D. Li, and E. Barsoum
  PARD: accelerating llm inference with low-cost parallel draft model adaptation.
  In International Conference on Learning Representations,
  Vol. 2026, pp. 144562–144579.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Arriola et al. (2025)
  M. Arriola, A. Gokaslan, J. T. Chiu, Z. Yang, Z. Qi, J. Han, S. S. Sahoo, and V. Kuleshov
  Block diffusion: interpolating between autoregressive and diffusion language models.
  In International Conference on Learning Representations,
  External Links: [Link](https://arxiv.org/abs/2503.09573)
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Austin et al. (2021)
  J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, et al.
  Program synthesis with large language models.
  arXiv preprint arXiv:2108.07732.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Bachmann et al. (2025)
  G. Bachmann, S. Anagnostidis, A. Pumarola, M. Georgopoulos, A. Sanakoyeu, Y. Du, E. Schönfeld, A. Thabet, and J. Kohler
  Judge decoding: faster speculative sampling requires going beyond model alignment.
  In International Conference on Learning Representations,
  External Links: [Link](https://proceedings.iclr.cc/paper_files/paper/2025/hash/656d6174fd5ffb01c843f269649ab5cb-Abstract-Conference.html)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Bai et al. (2025)
  Y. Bai, S. Tu, J. Zhang, H. Peng, X. Wang, X. Lv, S. Cao, J. Xu, L. Hou, Y. Dong, et al.
  Longbench v2: towards deeper understanding and reasoning on realistic long-context multitasks.
  In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
  pp. 3639–3664.
  Cited by: [§B.3](#A2.SS3.p2.1 "B.3 Long-context Evaluation Protocol ‣ Appendix B Experimental Setup Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.3](#S4.SS3.p1.1 "4.3 Long-context Tasks ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Cai et al. (2024)
  T. Cai, Y. Li, Z. Geng, H. Peng, J. D. Lee, D. Chen, and T. Dao
  Medusa: simple LLM inference acceleration framework with multiple decoding heads.
  In Forty-first International Conference on Machine Learning,
  External Links: [Link](https://openreview.net/forum?id=PEpbUobfJv)
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p3.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p2.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Chen et al. (2023)
  C. Chen, S. Borgeaud, G. Irving, J. Lespiau, L. Sifre, and J. Jumper
  Accelerating large language model decoding with speculative sampling.
  arXiv preprint arXiv:2302.01318.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p1.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Chen et al. (2026)
  J. Chen, Y. Liang, and Z. Liu
  DFlash: block diffusion for flash speculative decoding.
  In Forty-third International Conference on Machine Learning,
  External Links: [Link](https://openreview.net/forum?id=Oz335dV48X)
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [1st item](#S1.I1.i1.p1.1 "In 1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.2 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§3.1.1](#S3.SS1.SSS1.p1.2 "3.1.1 Unigram Proposer ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p2.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p3.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.2](#S4.SS2.p1.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p1.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Chen et al. (2021)
  M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, et al.
  Evaluating large language models trained on code.
  arXiv preprint arXiv:2107.03374.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Cheng et al. (2026)
  X. Cheng, X. Yu, C. Shao, J. Li, Y. Xiong, Y. Qian, J. Zhu, S. Ma, X. Zhang, J. Ye, et al.
  DSpark: confidence-scheduled speculative decoding with semi-autoregressive generation.
  arXiv preprint arXiv:2607.05147.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p4.2 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.2](#S4.SS2.p1.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p1.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Cobbe et al. (2021)
  K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al.
  Training verifiers to solve math word problems.
  arXiv preprint arXiv:2110.14168.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Devic et al. (2025)
  S. Devic, C. Peale, A. Bradley, S. Williamson, P. Nakkiran, and A. Gollakota
  Trace length is a simple uncertainty signal in reasoning models.
  arXiv preprint arXiv:2510.10409.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* DiffusionGemma Team et al. (2026)
  DiffusionGemma Team, A. A. Taïga, J. Assiene, D. Calandriello, R. Chaabouni, J. Gante, et al.
  DiffusionGemma technical report.
  arXiv preprint arXiv:2608.00146.
  External Links: [Link](https://arxiv.org/abs/2608.00146)
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Garipov et al. (2026)
  R. Garipov, F. Velikonivtsev, I. Ermakov, R. Svirschevski, V. Egiazarian, and M. Ryabinin
  Autojudge: judge decoding without manual annotation.
  Advances in Neural Information Processing Systems 38, pp. 94605–94642.
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Gloeckle et al. (2024)
  F. Gloeckle, B. Youbi Idrissi, B. Roziere, D. Lopez-Paz, and G. Synnaeve
  Better & faster large language models via multi-token prediction.
  In Proceedings of the 41st International Conference on Machine Learning,
  pp. 15706–15734.
  External Links: [Link](https://proceedings.mlr.press/v235/gloeckle24a.html)
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Holsman et al. (2025)
  M. Holsman, Y. Huang, and B. Dhingra
  Fuzzy speculative decoding for a tunable accuracy-runtime tradeoff.
  In Findings of the Association for Computational Linguistics: ACL 2025,
  pp. 26257–26273.
  External Links: [Document](https://dx.doi.org/10.18653/v1/2025.findings-acl.1346),
  [Link](https://aclanthology.org/2025.findings-acl.1346/)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Huang et al. (2026)
  J. Huang, Y. Zhang, Q. Zhang, H. Lin, H. Xu, and L. Zhang
  Domino: decoupling causal modeling from autoregressive drafting in speculative decoding.
  arXiv preprint arXiv:2605.29707.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p3.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p1.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Inception Labs et al. (2025)
  Inception Labs, S. Khanna, S. Kharbanda, S. Li, H. Varma, E. Wang, S. Birnbaum, Z. Luo, Y. Miraoui, A. Palrecha, S. Ermon, A. Grover, and V. Kuleshov
  Mercury: ultra-fast language models based on diffusion.
  arXiv preprint arXiv:2506.17298.
  External Links: [Link](https://arxiv.org/abs/2506.17298)
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Inco AI (2026)
  Inco AI
  DFlash 2: keep drafting parallel.
  External Links: [Link](https://inco.ai/blog/dflash2/)
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.2 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§3.1.1](#S3.SS1.SSS1.p1.2 "3.1.1 Unigram Proposer ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§3.1.2](#S3.SS1.SSS2.p1.1 "3.1.2 Bigram Selector ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.2](#S4.SS2.p1.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p1.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Jain et al. (2025)
  N. Jain, A. Gu, W. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica
  Livecodebench: holistic and contamination free evaluation of large language models for code.
  In International Conference on Learning Representations,
  Vol. 2025, pp. 58791–58831.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Jimenez et al. (2024)
  C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan
  SWE-bench: can language models resolve real-world GitHub issues?.
  In International Conference on Learning Representations,
  Cited by: [§B.3](#A2.SS3.p3.1 "B.3 Long-context Evaluation Protocol ‣ Appendix B Experimental Setup Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.3](#S4.SS3.p1.1 "4.3 Long-context Tasks ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Kim et al. (2023)
  S. Kim, K. Mangalam, S. Moon, J. Malik, M. W. Mahoney, A. Gholami, and K. Keutzer
  Speculative decoding with big little decoder.
  In Advances in Neural Information Processing Systems,
  Vol. 36.
  External Links: [Link](https://proceedings.neurips.cc/paper_files/paper/2023/hash/7b97adeafa1c51cf65263459ca9d0d7c-Abstract-Conference.html)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Kimi Team et al. (2025)
  Kimi Team, Y. Zhang, Z. Lin, X. Yao, J. Hu, F. Meng, et al.
  Kimi Linear: an expressive, efficient attention architecture.
  arXiv preprint arXiv:2510.26692.
  Cited by: [§4.2](#S4.SS2.p2.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Leviathan et al. (2023)
  Y. Leviathan, M. Kalman, and Y. Matias
  Fast inference from transformers via speculative decoding.
  In International conference on machine learning,
  pp. 19274–19286.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p1.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2026a)
  G. Li, Z. Fu, M. Fang, Q. Zhao, M. Tang, C. Yuan, and J. Wang
  Diffuspec: unlocking diffusion language models for speculative decoding.
  In Findings of the Association for Computational Linguistics: ACL 2026,
  pp. 20896–20910.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2026b)
  S. Li, C. Wang, Y. Zhu, Y. Wang, F. Yin, S. Shi, Y. Chen, X. Dong, Q. Chen, J. Pan, et al.
  SpecForge: a flexible and efficient open-source training framework for speculative decoding.
  arXiv preprint arXiv:2603.18567.
  Cited by: [§4.1](#S4.SS1.p2.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2026c)
  T. Li, Y. Luo, X. Shang, and Z. Shen
  DARTree: speculative diffusion decoding with autoregressive draft trees.
  arXiv preprint arXiv:2608.13524.
  Cited by: [Appendix A](#A1.p1.1 "Appendix A Tree Construction Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [Appendix A](#A1.p5.2 "Appendix A Tree Construction Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p3.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p3.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§3.1.3](#S3.SS1.SSS3.p1.1 "3.1.3 Tree Construction and Verification ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p2.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p3.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p5.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2024a)
  Y. Li, F. Wei, C. Zhang, and H. Zhang
  Eagle-2: faster inference of language models with dynamic draft trees.
  In Proceedings of the 2024 conference on empirical methods in natural language processing,
  pp. 7421–7432.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p3.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2024b)
  Y. Li, F. Wei, C. Zhang, and H. Zhang
  EAGLE: speculative sampling requires rethinking feature uncertainty.
  In Forty-first International Conference on Machine Learning,
  External Links: [Link](https://openreview.net/forum?id=1NdN7eXyb4)
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2026d)
  Y. Li, F. Wei, C. Zhang, and H. Zhang
  Eagle-3: scaling up inference acceleration of large language models via training-time test.
  Advances in Neural Information Processing Systems 38, pp. 136737–136756.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p3.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Lightman et al. (2024)
  H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
  Let’s verify step by step.
  In International Conference on Learning Representations,
  Vol. 2024, pp. 39578–39601.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Liu et al. (2025)
  A. Liu, M. He, S. Zeng, S. Zhang, L. Zhang, C. Wu, W. Jia, Y. Liu, X. Zhou, and J. Zhou
  WeDLM: reconciling diffusion language models with standard causal attention for fast inference.
  arXiv preprint arXiv:2512.22737.
  External Links: [Link](https://arxiv.org/abs/2512.22737)
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Liu et al. (2026)
  F. Liu, X. Li, K. Zhao, Y. Gao, Z. Zhou, Z. Zhang, Z. Wang, W. Dou, S. Zhong, and C. Tian
  DART: diffusion-inspired speculative decoding for fast llm inference.
  arXiv preprint arXiv:2601.19278.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Miao et al. (2024)
  X. Miao, G. Oliaro, Z. Zhang, X. Cheng, Z. Wang, Z. Zhang, R. Y. Y. Wong, A. Zhu, L. Yang, X. Shi, et al.
  Specinfer: accelerating large language model serving with tree-based speculative inference and verification.
  In Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 3,
  pp. 932–949.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p3.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p2.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Narasimhan et al. (2025)
  H. Narasimhan, W. Jitkrittum, A. S. Rawat, S. Kim, N. Gupta, A. K. Menon, and S. Kumar
  Faster cascades via speculative decoding.
  In International Conference on Learning Representations,
  External Links: [Link](https://proceedings.iclr.cc/paper_files/paper/2025/hash/6f43166f50f26e8d8f3edc5545b0749f-Abstract-Conference.html)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Nie et al. (2026)
  S. Nie, F. Zhu, Z. You, X. Zhang, J. Ou, J. Hu, J. Zhou, Y. Lin, J. Wen, and C. Li
  Large language diffusion models.
  Advances in Neural Information Processing Systems 38, pp. 50608–50646.
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Qwen Team (2026)
  Qwen Team
  Qwen3.8-Max: a new bar for coding and cowork.
  External Links: [Link](https://qwen.ai/blog?id=qwen3.8)
  Cited by: [§4.2](#S4.SS2.p1.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Ringel and Romano (2026)
  L. Ringel and Y. Romano
  Accelerating speculative decoding with block diffusion draft trees.
  arXiv preprint arXiv:2604.12989.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p3.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p3.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p3.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Wang et al. (2026a)
  L. Wang, Y. Su, X. Wu, C. You, Y. Liu, Z. Qiu, J. Zhang, J. Zheng, F. Liu, J. Zhang, et al.
  Bole: efficient tree speculation for hybrid-attention language models.
  arXiv preprint arXiv:2608.01651.
  Cited by: [§4.2](#S4.SS2.p2.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Wang et al. (2026b)
  Z. Wang, S. R. Kasa, A. M. S, S. K. Kasa, J. Zou, S. Negi, R. Zhang, N. Jiang, and Q. Song
  DIVERSED: relaxed speculative decoding via dynamic ensemble verification.
  In Proceedings of the 29th International Conference on Artificial Intelligence and Statistics,
  Vol. 300, pp. 2341–2349.
  External Links: [Link](https://proceedings.mlr.press/v300/wang26d.html)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Xie et al. (2025)
  Z. Xie, J. Ye, L. Zheng, J. Gao, J. Dong, Z. Wu, X. Zhao, S. Gong, X. Jiang, Z. Li, et al.
  Dream-coder 7b: an open diffusion language model for code.
  arXiv preprint arXiv:2509.01142.
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Xu et al. (2024)
  T. Xu, E. Helenowski, K. A. Sankararaman, D. Jin, K. Peng, E. Han, S. Nie, C. Zhu, H. Zhang, W. Zhou, et al.
  The perfect blend: redefining rlhf with mixture of judges.
  arXiv preprint arXiv:2409.20370.
  Cited by: [§4.1](#S4.SS1.p2.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.2](#S4.SS2.p1.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Yang et al. (2025a)
  A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, et al.
  Qwen3 technical report.
  arXiv preprint arXiv:2505.09388.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Yang et al. (2026)
  P. Yang, C. Du, F. Zhang, H. Wang, T. Pang, C. Du, and B. An
  LongSpec: long-context lossless speculative decoding with efficient drafting and verification.
  In Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
  pp. 1826–1844.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Yang et al. (2025b)
  S. Yang, J. Kautz, and A. Hatamizadeh
  Gated delta networks: improving mamba2 with delta rule.
  In International Conference on Learning Representations,
  Vol. 2025, pp. 29687–29707.
  Cited by: [§4.2](#S4.SS2.p2.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Zheng et al. (2023)
  L. Zheng, W. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. Xing, et al.
  Judging llm-as-a-judge with mt-bench and chatbot arena.
  Advances in neural information processing systems 36, pp. 46595–46623.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Zheng et al. (2024)
  L. Zheng, L. Yin, Z. Xie, C. Sun, J. Huang, C. H. Yu, S. Cao, C. Kozyrakis, I. Stoica, J. E. Gonzalez, et al.
  Sglang: efficient execution of structured language model programs.
  Advances in neural information processing systems 37, pp. 62557–62583.
  Cited by: [§4.1](#S4.SS1.p5.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.2](#S4.SS2.p2.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Zhou et al. (2024)
  Y. Zhou, K. Lyu, A. S. Rawat, A. K. Menon, A. Rostamizadeh, S. Kumar, J. Kagy, and R. Agarwal
  DistillSpec: improving speculative decoding via knowledge distillation.
  In International Conference on Learning Representations,
  External Links: [Link](https://openreview.net/forum?id=rsY6J3ZaTF)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Zhu et al. (2026)
  S. Zhu, X. Ye, H. Lu, W. Shi, and G. Liu
  The many faces of on-policy distillation: pitfalls, mechanisms, and fixes.
  arXiv preprint arXiv:2605.11182.
  Cited by: [§3.2](#S3.SS2.p3.1 "3.2 Tree-native Training ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").

## Appendix A Tree Construction Details

UBTree follows the search schedule of DARTree’s pruned variant (Algorithm 1 in [Li et al., 2026c](#bib.bib18)), reviewed in Section [2](#S2 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"). DARTree evaluates path-conditioned correction probabilities and updates correction states between depths; UBTree instead supplies precomputed proposer and selector scores, so these correction-state updates are not needed.

Path Scores.
For a fixed verified context x≤tx\_{\leq t}, we use the candidate sets from Section [3.1.1](#S3.SS1.SSS1 "3.1.1 Unigram Proposer ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") and combined scores from equation [5](#S3.E5 "In 3.1.2 Bigram Selector ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"). These scores incorporate both proposer logits and selector scores conditioned on the proposer’s hidden states. For each predecessor a∈𝒞i−1a\in\mathcal{C}\_{i-1}, normalization over successor candidates defines a conditional distribution, whose log-probabilities accumulate along a candidate path:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | qibi​(b∣a,x≤t)\displaystyle q\_{i}^{\mathrm{bi}}(b\mid a,x\_{\leq t}) | =exp⁡si​(a,b)∑v∈𝒞iexp⁡si​(a,v),b∈𝒞i,\displaystyle=\frac{\exp s\_{i}(a,b)}{\sum\_{v\in\mathcal{C}\_{i}}\exp s\_{i}(a,v)},\qquad b\in\mathcal{C}\_{i}, |  | (9) |
|  | ℓ(y1:d)\displaystyle\ell(y\_{1:d}) | =∑i=1dlog⁡qibi​(yi∣yi−1,x≤t).\displaystyle=\sum\_{i=1}^{d}\log q\_{i}^{\mathrm{bi}}(y\_{i}\mid y\_{i-1},x\_{\leq t}). |  |

Here, y0=xty\_{0}=x\_{t} and 1≤d≤γ1\leq d\leq\gamma is the path depth. The root represents the empty draft prefix ϵ\epsilon, with ℓ⁡(ϵ)=0\ell(\epsilon)=0. Each non-root node is identified by its complete draft prefix y1:dy\_{1:d}; identical tokens reached through different parents remain distinct nodes.

Depth Bonus.
Following DARTree’s scoring form, the search permits a nonpositive depth bonus when ranking tree nodes. The reported UBTree evaluations use ζ=0\zeta=0:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℓζ(y1:d)=ℓ(y1:d)+ζd,ζ=0.\ell\_{\zeta}(y\_{1:d})=\ell(y\_{1:d})+\zeta d,\qquad\zeta=0. |  | (10) |

We set ℓζ​(ϵ)=0\ell\_{\zeta}(\epsilon)=0 and use ζ\zeta to distinguish this depth bonus from the training-loss weight β\beta. The bonus is applied to path scores after probability normalization. It leaves rankings within each depth unchanged and penalizes deeper nodes during global pruning only when ζ<0\zeta<0.

Depth-Wise Expansion.
Let ℱd\mathcal{F}\_{d} be the retained frontier at depth dd, initialized by ℱ0={ϵ}\mathcal{F}\_{0}=\{\epsilon\}. At each depth, we extend every retained path with the candidates at that position and select the highest-scoring extensions:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | ℰd\displaystyle\mathcal{E}\_{d} | ={y1:d:y1:d−1∈ℱd−1,yd∈𝒞d},\displaystyle=\{y\_{1:d}:y\_{1:d-1}\in\mathcal{F}\_{d-1},\ y\_{d}\in\mathcal{C}\_{d}\}, |  | (11) |
|  | ℱd\displaystyle\mathcal{F}\_{d} | =TopW(ℰd;ℓζ),d=1,…,γ.\displaystyle=\operatorname{Top}\_{W}(\mathcal{E}\_{d};\ell\_{\zeta}),\qquad d=1,\ldots,\gamma. |  |

We interpret y1:0=ϵy\_{1:0}=\epsilon. The operator TopW⁡(ℰd;ℓζ)\operatorname{Top}\_{W}(\mathcal{E}\_{d};\ell\_{\zeta}) retains up to WW nodes with the largest depth-penalized scores across all extensions at depth dd, not WW children per parent. Scoring an extension adds its conditional log-probability from equation [9](#A1.E9 "In Appendix A Tree Construction Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") and ζ\zeta to its parent’s score using the precomputed combined scores, without another selector evaluation.

Global Pruning.
The retained frontiers form a candidate supertree. We select at most BB non-root nodes from this supertree by the same depth-penalized score:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒮=⋃d=1γℱd,𝒯={ϵ}∪TopB⁡(𝒮;ℓζ).\mathcal{S}=\bigcup\_{d=1}^{\gamma}\mathcal{F}\_{d},\qquad\mathcal{T}=\{\epsilon\}\cup\operatorname{Top}\_{B}(\mathcal{S};\ell\_{\zeta}). |  | (12) |

The root is kept separately and does not count toward BB. Since every normalized probability is at most one and ζ≤0\zeta\leq 0, ℓζ(y1:d)≤ℓζ(y1:d−1)\ell\_{\zeta}(y\_{1:d})\leq\ell\_{\zeta}(y\_{1:d-1}). Preferring ancestors when scores tie therefore ensures that every selected node retains all its ancestors, following the prefix-monotonicity argument in Lemma 1 of [Li et al. (2026c)](#bib.bib18). This selection is restricted to the materialized supertree 𝒮\mathcal{S}; finite-width expansion can discard paths before global pruning.

Construction Summary.
Algorithm [1](#alg1 "Algorithm 1 ‣ Appendix A Tree Construction Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") summarizes tree construction
from precomputed proposer and selector scores, without further
selector evaluation. We use y1:0=ϵy\_{1:0}=\epsilon and y0=xty\_{0}=x\_{t}.
The operator Topm\operatorname{Top}\_{m} retains up to mm
highest-scoring nodes, preferring ancestors when scores tie.

Algorithm 1  UBTree Construction from Precomputed Scores

1:
Input:
Verified context x≤tx\_{\leq t},
candidate sets {𝒞i}i=1γ\{\mathcal{C}\_{i}\}\_{i=1}^{\gamma},
precomputed combined scores {si}i=1γ\{s\_{i}\}\_{i=1}^{\gamma},
search width WW, and non-root node budget BB.

2:
Output:
A prefix-closed tree 𝒯\mathcal{T}
with at most BB non-root nodes.

3:
ζ←0\zeta\leftarrow 0

4:
Precompute all candidate-pair log-probabilities
log⁡qibi\log q\_{i}^{\mathrm{bi}} using equation [9](#A1.E9 "In Appendix A Tree Construction Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").

5:
ℱ0←{ϵ}\mathcal{F}\_{0}\leftarrow\{\epsilon\},
ℓζ​(ϵ)←0\ell\_{\zeta}(\epsilon)\leftarrow 0,
𝒮←∅\mathcal{S}\leftarrow\varnothing

6:
for d=1,…,γd=1,\ldots,\gamma do

7:
  ℰd←{y1:d:y1:d−1∈ℱd−1,yd∈𝒞d}\mathcal{E}\_{d}\leftarrow\{y\_{1:d}:y\_{1:d-1}\in\mathcal{F}\_{d-1},\ y\_{d}\in\mathcal{C}\_{d}\}

8:
  for all y1:d∈ℰdy\_{1:d}\in\mathcal{E}\_{d} do

9:
   ℓζ(y1:d)←ℓζ(y1:d−1)+logqdbi(yd∣yd−1,x≤t)+ζ\ell\_{\zeta}(y\_{1:d})\leftarrow\ell\_{\zeta}(y\_{1:d-1})+\log q\_{d}^{\mathrm{bi}}(y\_{d}\mid y\_{d-1},x\_{\leq t})+\zeta

10:
  end for

11:
  ℱd←TopW⁡(ℰd;ℓζ)\mathcal{F}\_{d}\leftarrow\operatorname{Top}\_{W}(\mathcal{E}\_{d};\ell\_{\zeta})

12:
  𝒮←𝒮∪ℱd\mathcal{S}\leftarrow\mathcal{S}\cup\mathcal{F}\_{d}

13:
end for

14:
𝒯←{ϵ}∪TopB⁡(𝒮;ℓζ)\mathcal{T}\leftarrow\{\epsilon\}\cup\operatorname{Top}\_{B}(\mathcal{S};\ell\_{\zeta})

15:
return 𝒯\mathcal{T}

Verification via Tree-attention.
After tree construction, we verify the prefix-closed draft tree with at most B=64B=64 non-root nodes in a single target-model forward pass using tree attention. Each node is evaluated under its corresponding autoregressive prefix, and verification follows the child matching the target-model sample at each step until the first mismatch. The first unmatched sample is retained as the bonus token. After verification, the KV cache and recurrent states along the accepted path are carried forward to the next decoding round, while those of all other branches are discarded. Since every committed token is sampled from the target model under exactly the same prefix as in standard autoregressive decoding, the procedure is lossless.

## Appendix B Experimental Setup Details

We provide additional training and evaluation settings for the academic-scale experiments, long-context evaluations, and ablations in Section [4](#S4 "4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").

### B.1 Training and Inference Configuration

Table [5](#A2.T5 "Table 5 ‣ B.1 Training and Inference Configuration ‣ Appendix B Experimental Setup Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") summarizes the configuration for the academic-scale experiments. We initialize the depth-calibration parameters to ρi=κi=0\rho\_{i}=\kappa\_{i}=0, so the proposer logits and selector scores initially have unit weights. Academic-scale inference loads the target and drafter weights in BF16 and captures draft post-processing in a single CUDA Graph.

Table 5: UBTree configuration for the academic-scale experiments, unless otherwise specified. The verification budget excludes the anchor.

|  |  |
| --- | --- |
| Setting | Value |
| Proposer training | 6 epochs |
| Joint proposer–selector training | 2 epochs |
| Selector rank | 256 |
| Codebook MLP hidden width | 1024 |
| Training candidate support size | 256 |
| Draft depth | 15 future positions plus an anchor |
| Candidate tokens per position KK | 64 |
| Search width WW | 12 |
| Verification budget BB | 64 non-root nodes |
| Depth bonus ζ\zeta | 00 |

### B.2 Evaluation and Timing Protocol

For our academic-scale evaluations, we use fixed seed-0 subsets with the sample counts listed in Table [6](#A2.T6 "Table 6 ‣ B.2 Evaluation and Timing Protocol ‣ Appendix B Experimental Setup Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"). Each configuration is evaluated once on the selected subset. Generation stops at EOS or after 2,048 new tokens. MT-Bench contains 80 two-turn dialogues, yielding 160 evaluated turns.

For each question or dialogue turn, time per output token (TPOT) is computed from the elapsed decoding time and the output-token count within the same timing window. The same decoding-time measurement protocol is used for all locally evaluated methods and the autoregressive baseline. Within each benchmark, speedup is the ratio of the mean autoregressive TPOT to the mean speculative-decoding TPOT. Acceptance length is averaged over questions or dialogue turns.

Table 6: Evaluation subset sizes. MT-Bench contains two-turn dialogues; the other counts refer to individual examples.

| Benchmark | Examples / dialogues |
| --- | --- |
| GSM8K | 128 |
| MATH-500 | 128 |
| AIME | 30 |
| HumanEval | 128 |
| MBPP | 128 |
| LiveCodeBench | 128 |
| MT-Bench | 80 |

### B.3 Long-context Evaluation Protocol

Shared Settings.
We compare UBTree with DSpark and DFlash on Ling3-Flash using the serving configuration in Section [4.2](#S4.SS2 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"): tensor parallelism of degree 4 on four H200 GPUs, greedy decoding, and thinking disabled. Both long-context evaluations use concurrency 1 with CUDA Graphs disabled. We measure root-inclusive acceptance length τ\tau as the number of generated tokens per target verification call, including the target-produced token. All methods use a maximum draft depth of 7, giving a maximum acceptance length of 8. DSpark and DFlash verify a single chain, while UBTree uses a budget of 64 non-root tree nodes per round.

LongBench-v2.
We evaluate long-input generation on LongBench-v2 ([Bai et al., 2025](#bib.bib34)). From the 503 source examples, we retain the same 401 requests with at most 260K prompt tokens for all methods. Generation stops at EOS or after 2,048 new tokens. We group requests by their prompt length before generation into six context-length bins with upper boundaries of 32K, 64K, 96K, 128K, 192K, and 260K tokens. Each bin contains the naturally occurring benchmark inputs in that length range. Table [8](#A3.T8 "Table 8 ‣ C.2 Long-context Tasks ‣ Appendix C Additional Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") reports acceptance length and request counts for these bins, together with results over the full evaluation subset.

SWE-bench.
We evaluate acceptance as agent histories grow on SWE-bench ([Jimenez et al., 2024](#bib.bib35)). We first run target-only inference on 30 cases and freeze the resulting 1,482 complete requests. Each method then replays the identical recorded messages, tool calls, and tool outputs with a fixed generation limit of 256 tokens. This shared replay protocol aligns the agent context across methods at every request. To match the context-length axis in Figure [1](#S0.F1 "Figure 1 ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding")(c), we group requests by the increase in prompt tokens relative to the first request of the corresponding case, using bins ≤0\leq 0, 0–4K, 4–8K, 8–16K, 16–32K, 32–64K, and 64–131K. The ≤0\leq 0 bin contains requests whose prompt length is no greater than the initial prompt, including context truncation or reconstruction events. Table [9](#A3.T9 "Table 9 ‣ C.2 Long-context Tasks ‣ Appendix C Additional Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") reports acceptance length and the number of cases represented in each bin; its Overall column reports request-pooled acceptance length over all 1,482 requests.

As a complementary analysis, we summarize the same replay requests by trajectory progress. We divide each case chronologically into four stages containing approximately equal numbers of requests: 0–25%, 25–50%, 50–75%, and 75–100%. Within each case and stage, we compute acceptance length as total generated tokens divided by total target verification calls, then average equally across the 30 cases. These stages measure relative progress through an agent trajectory. Since the amount of context added per request varies across cases and requests, the stage boundaries do not correspond to fixed context lengths.

### B.4 Ablation Protocol

For the training-temperature ablation in Table [4](#S4.T4 "Table 4 ‣ 4.3 Long-context Tasks ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"), we regenerate target responses at each TtrainT\_{\mathrm{train}} and use them for both proposer training and joint proposer–selector training. Each joint run starts from the proposer trained at the corresponding temperature. The target distribution for KL supervision uses the same TtrainT\_{\mathrm{train}}, following Eq. equation [7](#S3.E7 "In 3.2 Tree-native Training ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"). Across temperatures, we retain the same selector architecture, training configuration, and tree-search configuration. Each resulting checkpoint is evaluated at both Tinfer=0T\_{\mathrm{infer}}=0 and Tinfer=1T\_{\mathrm{infer}}=1. For the training-objective ablation, all variants start from the same proposer checkpoint and use identical training responses. Hard-label selector CE excludes positions whose sampled target token falls outside the training candidate support, whereas forward KL supervises all valid positions.

## Appendix C Additional Experiments

### C.1 Drafting Latency Analysis

We profile Qwen3-4B using Hugging Face Transformers-based implementations on 128 GSM8K questions at Tinfer=0T\_{\mathrm{infer}}=0, using the search budgets in Section [4.1](#S4.SS1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"). For each question, all methods run on the same H200 GPU in randomized order, and we average measurements over ten complete passes. Timing excludes prefill and the first complete speculative round. Stage latencies are measured with CUDA events, while total round latency is measured independently using synchronized wall-clock time. For UBTree, draft post-processing includes LM-head projection, candidate selection, selector scoring, and tree construction, which are timed jointly. The ms/token column reports TPOT averaged over questions.

Table [7](#A3.T7 "Table 7 ‣ C.1 Drafting Latency Analysis ‣ Appendix C Additional Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") shows that UBTree reduces draft post-processing latency from DARTree’s 3.36 ms to 1.38 ms per round, a reduction of 58.8%, while target verification takes approximately 20.9 ms for both methods. The principal latency reduction therefore occurs on the parallel selector side. UBTree achieves a higher acceptance length than DARTree (12.58 versus 12.50) while reducing decoding latency from 2.41 to 2.21 ms per token.

Table 7: Drafting Latency profiling on Qwen3-4B. Stage and total latencies are in ms per verification round.

| Method | Proposer stage | Draft post-processing | Verification | Other | Total | τ\tau | ms/token |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DARTree | 3.51 | 3.36 | 20.94 | 1.64 | 29.47 | 12.50 | 2.41 |
| UBTree | 3.41 | 1.38 | 20.88 | 1.61 | 27.30 | 12.58 | 2.21 |

### C.2 Long-context Tasks

Tables [8](#A3.T8 "Table 8 ‣ C.2 Long-context Tasks ‣ Appendix C Additional Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") and [9](#A3.T9 "Table 9 ‣ C.2 Long-context Tasks ‣ Appendix C Additional Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding") report the quantitative results underlying Figure [1](#S0.F1 "Figure 1 ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding")(c), together with the overall acceptance length on each benchmark. All results follow the long-context evaluation protocol in Appendix [B.3](#A2.SS3 "B.3 Long-context Evaluation Protocol ‣ Appendix B Experimental Setup Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").

Table 8: Acceptance length (τ\tau) on LongBench-v2 with Ling3-Flash, grouped by request-start prompt length. All methods use the same 401 requests. The Overall column reports results over the full evaluation subset. Bold marks the best acceptance length per column.

| Prompt tokens | ≤32\leq 32K | 32–64K | 64–96K | 96–128K | 128–192K | 192–260K | Overall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Requests | 109 | 71 | 47 | 69 | 73 | 32 | 401 |
| DSpark | 4.248 | 4.297 | 3.795 | 3.976 | 4.166 | 4.084 | 4.136 |
| DFlash | 4.020 | 4.046 | 3.578 | 3.678 | 3.944 | 3.919 | 3.898 |
| UBTree | 5.833 | 5.870 | 5.326 | 5.351 | 5.798 | 5.804 | 5.693 |

Table 9: Acceptance length (τ\tau) on SWE-bench with Ling3-Flash, grouped by accumulated prompt tokens relative to the first request in each case. Covered cases gives the number of cases represented in each bin. The Overall column reports request-pooled acceptance length over all 1,482 requests from 30 cases. Bold marks the best acceptance length per column.

| Accumulated tokens | ≤0\leq 0 | 0–4K | 4–8K | 8–16K | 16–32K | 32–64K | 64–131K | Overall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Covered cases | 30 | 30 | 28 | 27 | 23 | 13 | 2 | 30 |
| DSpark | 3.718 | 3.743 | 4.023 | 3.998 | 4.089 | 4.023 | 3.965 | 3.981 |
| DFlash | 3.442 | 3.524 | 3.795 | 3.709 | 3.836 | 3.805 | 3.770 | 3.737 |
| UBTree | 4.842 | 4.829 | 5.447 | 5.389 | 5.516 | 5.408 | 5.465 | 5.341 |

Results.
UBTree achieves the highest acceptance length in every context-length bin on both benchmarks. On LongBench-v2, UBTree reaches τ=5.326\tau=5.326–5.8705.870, improving over the strongest baseline, DSpark, by 34.634.6–42.1%42.1\%. At 192–260K prompt tokens, UBTree attains τ=5.804\tau=5.804, compared with 4.084 for DSpark and 3.919 for DFlash, retaining nearly the same acceptance length as in the shortest bin (5.8335.833). Overall, UBTree achieves τ=5.693\tau=5.693, a 37.6%37.6\% improvement over DSpark. On SWE-bench, UBTree reaches τ=4.829\tau=4.829–5.5165.516 across accumulated-context bins, exceeding DSpark by 29.029.0–37.8%37.8\%. Its overall request-pooled acceptance length is 5.3415.341, compared with 3.9813.981 for DSpark and 3.7373.737 for DFlash, improving over the strongest baseline by 34.2%34.2\%. These results demonstrate UBTree’s sustained acceptance advantage across both long initial prompts and growing agent histories.

Trajectory-stage Results.
Under the complementary trajectory-stage aggregation defined in Appendix [B.3](#A2.SS3 "B.3 Long-context Evaluation Protocol ‣ Appendix B Experimental Setup Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"), UBTree achieves acceptance lengths of 5.043, 5.364, 5.348, and 5.476 across the four successive SWE-bench stages, compared with 3.835, 3.989, 3.942, and 3.999 for the strongest baseline, DSpark. The corresponding gains range from 31.5%31.5\% to 36.9%36.9\%. This summary captures UBTree’s advantage throughout agent trajectories, while the 29.029.0–37.8%37.8\% gains reported in the main text correspond to the accumulated-context results in Table [9](#A3.T9 "Table 9 ‣ C.2 Long-context Tasks ‣ Appendix C Additional Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"). The two ranges summarize the same replay workload under different groupings.

## Appendix D Limitations

Despite UBTree’s strong empirical performance, two limitations remain.

Tree drafting is sensitive to very high concurrency.
Speculative decoding is motivated by the spare compute available when autoregressive inference is limited by memory bandwidth, as is common in LLM decoding. Verifying multiple draft tokens together uses this capacity to amortize memory-access costs. As concurrency increases and inference becomes compute-bound, the spare capacity available for speculation shrinks, potentially eliminating speedups for both single-path and tree-based methods. Sensitivity to this transition is shared by all tree-based drafters and is not specific to UBTree. Tree verification spends additional compute on alternative continuations and therefore favors the part of the compute–bandwidth spectrum with more spare compute. Adaptive tree drafting can mitigate this limitation by varying the verification budget with available compute: branching allows the number of verified candidates to vary beyond the token count of a fixed single-path block, although the proposer block size still bounds draft depth. Our load-dependent tree budgets already retain speedups at the tested concurrency levels (Table [2](#S4.T2 "Table 2 ‣ 4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding")), and more flexible runtime adaptation could further improve resource use. UBTree can also serve low-concurrency workloads where spare compute is abundant. We therefore view this limitation as a constraint on the favorable deployment regime, rather than a fundamental obstacle to UBTree’s practical value.

Adaptive tree strategies rely on searched configurations.
Our current adaptive strategy uses tree budgets BB and search widths WW selected through configuration search for each model and concurrency level. These settings are fixed for a given serving load; they do not determine the budget from the transition-score distribution of each decoding round. Although the tree’s contents depend on the predicted scores, the budget-selection policy remains empirically tuned and is not guaranteed to be optimal as prediction uncertainty and available compute change. A more principled strategy would select tree sizes at each decoding round using calibrated estimates of acceptance benefit derived from transition scores, together with a cost model reflecting hardware and serving load. We leave developing and evaluating such a policy to future work.

## Appendix E Additional Related Work

Speculative Decoding. In addition to autoregressive ([Leviathan et al., 2023](#bib.bib8); [Chen et al., 2023](#bib.bib9); [Li et al., 2024b](#bib.bib12)), parallel ([Chen et al., 2026](#bib.bib5); [Liu et al., 2026](#bib.bib15); [Inco AI, 2026](#bib.bib17)), semi-autoregressive ([Huang et al., 2026](#bib.bib7); [Cheng et al., 2026](#bib.bib16)), and tree-based ([Cai et al., 2024](#bib.bib10); [Miao et al., 2024](#bib.bib11); [Li et al., 2024a](#bib.bib13); [Li et al., 2026d](#bib.bib6); [Ringel and Romano, 2026](#bib.bib19); [Li et al., 2026c](#bib.bib18)) drafting methods mentioned, existing research also explored mixing methods for speculative decoding. PARD adapts autoregressive models for parallel token prediction ([An et al., 2026](#bib.bib14)), while DiffuSpec uses pretrained diffusion language models as drafters ([Li et al., 2026a](#bib.bib27)).

Lossy Acceleration for Large Language Models.
Lossy acceleration reduces inference cost by allowing deviations from the target model’s output distribution. BiLD ([Kim et al., 2023](#bib.bib37)) coordinates small and large models through confidence-based fallback and discrepancy-based rollback. The lossy extension of DistillSpec ([Zhou et al., 2024](#bib.bib38)) relaxes token acceptance using a lenience factor, while Fuzzy Speculative Decoding ([Holsman et al., 2025](#bib.bib42)) bases acceptance on divergence between draft and target distributions. Speculative cascades ([Narasimhan et al., 2025](#bib.bib39)) implement model-deferral rules through speculative execution, selecting between draft and target distributions; DIVERSED ([Wang et al., 2026b](#bib.bib43)) instead learns context-dependent mixtures of these distributions for verification. Judge Decoding ([Bachmann et al., 2025](#bib.bib40); [Garipov et al., 2026](#bib.bib44)) accepts otherwise-rejected tokens using a lightweight correctness classifier on target hidden states. In contrast to these relaxed verification methods, UBTree improves candidate coverage and path quality through joint proposer–selector training while retaining target-distribution-preserving verification.

Multi-token Language Models for Fast Generation.
Another line of work incorporates multi-token prediction into the language model itself. [Gloeckle et al. (2024)](#bib.bib41) train multiple prediction heads on a shared backbone to predict several future tokens simultaneously. Diffusion language models, including LLaDA ([Nie et al., 2026](#bib.bib1)) and Dream ([Xie et al., 2025](#bib.bib2)), learn to recover masked tokens and generate text through iterative parallel denoising. LLaDA is trained from scratch, whereas Dream adapts pretrained autoregressive weights. Block diffusion ([Arriola et al., 2025](#bib.bib4)) combines autoregressive generation across blocks with parallel denoising within each block, enabling flexible-length generation and prefix KV caching. Large-scale block diffusion with different recipes enriches the explored space of taming diffusion for multi-token fast generation, including WeDLM ([Liu et al., 2025](#bib.bib3)), Mercury ([Inception Labs et al., 2025](#bib.bib45)), and DiffusionGemma ([DiffusionGemma Team et al., 2026](#bib.bib46)). These approaches modify the generative model or its training to enable multi-token generation, while having the risk of degrading the sample quality.
