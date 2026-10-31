---
title: "IDM: Intrinsic Distribution Matching"
arxiv: 2610.39633
date: 2026-10-29
source: https://arxiv.org/abs/2610.39633
project: https://github.com/inclusionAI/IDM
crawled: 2026-10-31
---

# IDM: Intrinsic Distribution Matching

> 原文：[IDM: Intrinsic Distribution Matching](https://arxiv.org/abs/2610.39633) · InclusionAI · Westlake University 等 · arXiv

## Abstract

One-step and few-step text-to-image generation must accurately render the details specified in the prompt despite limited opportunities for refinement.
Distribution matching distillation (DMD) uses score differences to bring the generated distribution closer to a reference distribution.
Following prior work, we estimate this difference with internal velocity branches, avoiding a separate fake-score network.
We ask whether an explicit moment constraint improves this learned score supervision.
A decomposition of the reverse-KL field into a Gaussian moment component and a non-Gaussian residual identifies statistics that can be constrained explicitly.
We introduce Intrinsic Distribution Matching (IDM), which retains the full DMD correction and matches feature means and per-coordinate standard deviations using the generator’s exponential-moving-average (EMA) copy, requiring no external feature encoder.
Experiments use full-parameter and low-rank adaptation (LoRA) tuning on Z-Image-Turbo 6B and Qwen-Image 20B.
At two network evaluations, IDM reaches 94.25% and 90.20% on Chinese and English LongText-Bench, the highest scores among the compared methods at this budget.
Controlled ablations show gains from the added moment loss, while generator EMA features perform competitively with an external DINOv2 encoder across the five reported metrics.
Code is available [here](https://github.com/inclusionAI/IDM).

††corref: cor:population\_vel\_score††footnotetext: Equal contribution.\*\*footnotetext: Corresponding author.

## 1 Introduction

Diffusion and flow-matching models produce high-quality images, but their repeated network evaluations impose substantial inference cost ([Ho et al., 2020](#bib.bib12); [Song et al., 2020](#bib.bib13); [Lipman et al., 2022](#bib.bib10); [Liu et al., 2023](#bib.bib9)). One and few-step generation reduces this cost by learning a much shorter sampling process. The challenge is to accurately render the details specified in the prompt using only one or a few sampling steps. Long-text rendering makes this challenge concrete: many characters must remain legible and correct within a coherent image ([Geng et al., 2025b](#bib.bib83); [Wu et al., 2025a](#bib.bib33)). It therefore provides a demanding test of whether fast generation retains detailed conditional information.

Distribution matching distillation (DMD) trains a fast generator to match a reference distribution ([Yin et al., 2024b](#bib.bib16); [Yin et al., 2024a](#bib.bib14)). A score describes the local direction of increasing log density. A pretrained teacher supplies the reference score, while an auxiliary fake-score network estimates the score of the current generated distribution. Their difference guides updates to generated samples. These updates are applied sample by sample, but their direction depends on both distributions. Distribution matching can complement trajectory-based training: rCM combines score regularization with continuous-time consistency training ([Zheng et al., 2025](#bib.bib66)).

Figure 1: Overview of IDM for one-step generation.
Multi-step sampling refines samples iteratively, whereas one-step generation learns a direct noise-to-data map.
IDM combines an internal DMD loss with a feature-moment loss in the generator’s EMA feature space.
The right panel illustrates idealized alignment with single-evaluation inference.

TwinFlow and APEX obtain this score difference from internally separated velocity branches of the generator ([Cheng et al., 2025](#bib.bib56); [Liu et al., 2026a](#bib.bib61)). The model-score estimate is still learned, but no separate fake-score network is needed. We adopt this internal construction and ask whether the generator can also supply an explicit constraint on statistics across samples. Although the exact DMD field contains full distributional information, learned score estimates and finite training can leave discrepancies that an additional statistical objective may help reduce.

To motivate such a constraint, we revisit the reverse-KL score difference underlying DMD. Building on the Gaussian-plus-residual score representation ([Wang and Vastola, 2023](#bib.bib79); [Wang and Vastola, 2024](#bib.bib80)), we separate a component determined by means and covariances from the remaining score structure in [Section 3.3](#S3.SS3 "3.3 Decomposition of the Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching"). This identifies statistics that can be constrained explicitly, while showing why moments alone do not determine the full distribution. We therefore retain the full DMD correction and add a moment loss, testing its benefit through controlled ablations in a shared training setting.

We introduce Intrinsic Distribution Matching (IDM), which augments internal DMD with moment matching in the generator’s own feature space. Its exponential-moving-average (EMA) copy provides a shared representation for generated and reference samples; we match the means and per-coordinate standard deviations of these features. Unlike objectives that obtain features from an external encoder or teacher ([Yang et al., 2026](#bib.bib65); [Zhang et al., 2026b](#bib.bib67)), this design reuses the generator for both score estimation and feature extraction. Both training signals are obtained from the generator and its EMA copy, without a separate discriminator, score model, or external feature encoder.

We evaluate IDM using Z-Image-Turbo 6B and Qwen-Image 20B with full-parameter and LoRA tuning in [Section 5](#S5 "5 Experiments ‣ Intrinsic Distribution Matching"). LongText-Bench evaluates the Chinese and English long-text rendering fidelity emphasized above, with subsets denoted LongText-CN and LongText-EN ([Geng et al., 2025b](#bib.bib83)). At two network evaluations (2 NFE), IDM on Z-Image-Turbo achieves state-of-the-art scores among the compared methods: 94.25% and 90.20%, improving over Z-Image-Turbo++ by 2.63 and 0.32 percentage points, respectively in [Table 5](#S5.T5 "Table 5 ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching").

Our main contributions are:

1. a.

   Intrinsic distributional supervision. We augment internal DMD with an explicit loss on the means and per-coordinate standard deviations of generator EMA features. This adds statistical supervision across samples without a separate external feature encoder.
2. b.

   Distribution-gradient explanation. Building on the Gaussian-plus-residual score representation, we motivate an explicit moment constraint alongside the full DMD correction.
3. c.

   Few-step training and evaluation. We demonstrate full-parameter and LoRA training on 6B and 20B backbones. Ablations assess the added moment loss, EMA features, and regression choices, while LongText-Bench evaluates fine-grained text fidelity.

![Refer to caption](2610.39633v1/fig1_merged.png)

Figure 2: IDM (Z-Image), 2 NFE. Text rendering and portrait generation.

## 2 Background

##### Continuous Generative Models.

Diffusion and flow-matching models transform noise into data through repeated network evaluations ([Ho et al., 2020](#bib.bib12); [Song et al., 2020](#bib.bib13); [Lipman et al., 2022](#bib.bib10)). Distillation learns a shorter process ([Salimans and Ho, 2022](#bib.bib54); [Song et al., 2023](#bib.bib52)). We use rectified flow to define the generator and then explain the DMD supervision used to train it.

##### Rectified Flow and Few-Step Generation.

Let pz=𝒩⁡(𝟎,𝐈d)p\_{z}=\mathcal{N}(\mathbf{0},\mathbf{I}\_{d}) be the noise distribution and prp\_{r} the reference-data distribution. Rectified flow uses the path 𝐱r,t=(1−t)​𝐱r+t​ϵ\mathbf{x}\_{r,t}=(1-t)\mathbf{x}\_{r}+t\bm{\epsilon}, with independently sampled 𝐱r∼pr\mathbf{x}\_{r}\sim p\_{r} and ϵ∼pz\bm{\epsilon}\sim p\_{z} ([Liu et al., 2023](#bib.bib9)). Thus t=0t=0 denotes clean data and t=1t=1 pure noise.
A network 𝑭θ​(𝐱r,t,t,𝐜)\bm{F}\_{\theta}(\mathbf{x}\_{r,t},t,\mathbf{c}) regresses the pair velocity ϵ−𝐱r\bm{\epsilon}-\mathbf{x}\_{r}, where 𝐜∈𝒞\mathbf{c}\in\mathcal{C} is a text-conditioning vector. At the squared-error optimum it recovers the marginal velocity, the conditional average of pair velocities at the same noisy input and condition.
Few-step generation integrates this field from t=1t=1 to t=0t=0 with a small number of forward-Euler steps. At one network evaluation, the generator is Gθ​(𝐳,𝐜)=𝐳−𝑭θ​(𝐳,1,𝐜)G\_{\theta}(\mathbf{z},\mathbf{c})=\mathbf{z}-\bm{F}\_{\theta}(\mathbf{z},1,\mathbf{c}) for 𝐳∼pz\mathbf{z}\sim p\_{z}.

##### Distribution Matching Distillation.

The generator induces a distribution pθp\_{\theta}. DMD aims to match it to prp\_{r} through the reverse-KL gradient ([Wang et al., 2023](#bib.bib74); [Yin et al., 2024b](#bib.bib16)). At a fixed condition and noise level t∈(0,1)t\in(0,1), let pθ,tp\_{\theta,t} and pr,tp\_{r,t} be their noised distributions. A score 𝐬i,t=∇𝐱t​log​pi,t\mathbf{s}\_{i,t}=\nabla\_{\mathbf{x}\_{t}}\log p\_{i,t} points locally toward increasing log density. Evaluated at the same noised model sample, 𝐬r,t−𝐬θ,t\mathbf{s}\_{r,t}-\mathbf{s}\_{\theta,t} points toward a lower model-to-reference density ratio in [Section 3.1](#S3.SS1 "3.1 Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching").
The reference score is supplied by a frozen pretrained teacher. Since the generator provides samples but no tractable score, DMD trains a separate *fake-score network* on its outputs. This network estimates the generated distribution; the generator itself produces the images. The fake-score estimate must track the changing generator. The reference score guides samples toward regions supported by the target, while the model score accounts for the generator’s current concentration of probability mass. Both enter the distributional update, so the model score must still be learned when a separate network is removed.

##### Score–Velocity Identity.

For independent 𝐱∼p\mathbf{x}\sim p and ϵ∼pz\bm{\epsilon}\sim p\_{z}, set 𝐱t=(1−t)​𝐱+t​ϵ\mathbf{x}\_{t}=(1-t)\mathbf{x}+t\bm{\epsilon}. For t∈(0,1)t\in(0,1), the score 𝐬t:=∇𝐱t​log​pt\mathbf{s}\_{t}:=\nabla\_{\mathbf{x}\_{t}}\log p\_{t} and marginal velocity 𝐯t∗​(𝐱t):=𝔼⁡[ϵ−𝐱∣𝐱t]\mathbf{v}\_{t}^{\*}(\mathbf{x}\_{t}):=\mathbb{E}[\bm{\epsilon}-\mathbf{x}\mid\mathbf{x}\_{t}] satisfy

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐬t​(𝐱t)=−𝐱t+(1−t)​𝐯t∗​(𝐱t)t.\mathbf{s}\_{t}(\mathbf{x}\_{t})=-\frac{\mathbf{x}\_{t}+(1-t)\mathbf{v}\_{t}^{\*}(\mathbf{x}\_{t})}{t}\,. |  | (1) |

Thus a velocity estimate also provides a score estimate in [Appendix B.3](#A2.SS3 "B.3 Score–Velocity Identity ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"). Subtracting two velocities at the same input gives a scaled score difference.

##### Internal Score Estimation.

TwinFlow and APEX use two internally separated velocity branches of one generator to estimate the reference and model scores ([Cheng et al., 2025](#bib.bib56); [Liu et al., 2026a](#bib.bib61)). This removes the separate fake-score network while retaining model-score learning. Following APEX, we use this construction for DMD in [Section 4.1](#S4.SS1 "4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching"). We next examine the statistics represented by its target field to motivate additional supervision from the generator’s features.

## 3 A Distribution-Gradient View

The score difference in DMD defines a direction for changing the generated distribution. Separating the contribution of means and covariances from the remaining score structure clarifies what moment matching can constrain and why the full DMD correction is still needed.

### 3.1 Reverse-KL Field

The one-step generator maps 𝐳∼pz\mathbf{z}\sim p\_{z} to 𝐱θ=Gθ​(𝐳,𝐜)\mathbf{x}\_{\theta}=G\_{\theta}(\mathbf{z},\mathbf{c}), inducing pθ(⋅∣𝐜)p\_{\theta}(\cdot\mid\mathbf{c}); pr(⋅∣𝐜)p\_{r}(\cdot\mid\mathbf{c}) is the reference law. Here 𝐱\mathbf{x} is a sample in the generator’s output representation, and conditions follow pcp\_{c} independently of 𝐳\mathbf{z}.
For differentiable positive densities, define 𝐬i​(𝐱∣𝐜):=∇𝐱​log​pi​(𝐱∣𝐜)\mathbf{s}\_{i}(\mathbf{x}\mid\mathbf{c}):=\nabla\_{\mathbf{x}}\log p\_{i}(\mathbf{x}\mid\mathbf{c}), i∈{r,θ}i\in\{r,\theta\}. At fixed 𝐜\mathbf{c}, the reverse KL is

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒟KL(pθ∥pr)=∫pθ(𝐱∣𝐜)logpθ​(𝐱∣𝐜)pr​(𝐱∣𝐜)d𝐱.\mathcal{D}\_{\mathrm{KL}}(p\_{\theta}\|p\_{r})=\int p\_{\theta}(\mathbf{x}\mid\mathbf{c})\log\frac{p\_{\theta}(\mathbf{x}\mid\mathbf{c})}{p\_{r}(\mathbf{x}\mid\mathbf{c})}\,\mathrm{d}\mathbf{x}. |  | (2) |

Its sample-space distribution gradient is

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐠KL​(𝐱∣𝐜)=𝐬θ​(𝐱∣𝐜)−𝐬r​(𝐱∣𝐜).\mathbf{g}\_{\mathrm{KL}}(\mathbf{x}\mid\mathbf{c})=\mathbf{s}\_{\theta}(\mathbf{x}\mid\mathbf{c})-\mathbf{s}\_{r}(\mathbf{x}\mid\mathbf{c}). |  | (3) |

The descent direction is −𝐠KL=𝐬r−𝐬θ-\mathbf{g}\_{\mathrm{KL}}=\mathbf{s}\_{r}-\mathbf{s}\_{\theta}, pointing locally toward a lower model-to-reference density ratio. It changes as the generator distribution changes.
Applying the same identity to pθ,tp\_{\theta,t} and pr,tp\_{r,t} gives 𝐠KL,t=𝐬θ,t−𝐬r,t\mathbf{g}\_{\mathrm{KL},t}=\mathbf{s}\_{\theta,t}-\mathbf{s}\_{r,t}, the noisy field estimated in DMD. We state the identities below for clean laws under the regularity assumptions in [Appendix B.1](#A2.SS1 "B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"); the decomposition also applies to the noisy laws at each fixed tt, with their own means, covariances, and score residuals.

Figure 3: Reverse-KL Field Decomposition.
The full field 𝐠KL=𝐬θ−𝐬r\mathbf{g}\_{\mathrm{KL}}=\mathbf{s}\_{\theta}-\mathbf{s}\_{r} (left) is the sum of a Gaussian moment component (middle) and a non-Gaussian residual component (right). Solid contours show pip\_{i} and dashed contours its moment-matched Gaussian qiq\_{i}, for i∈{r,θ}i\in\{r,\theta\}.
Equal means and covariances eliminate the Gaussian component but can leave a nonzero residual. All fields use the same evaluation points and arrow scale.

### 3.2 Parameter Gradient

The field above specifies a sample update. To relate it to training, consider a discrepancy 𝒟⁡(pθ,pr)\mathcal{D}(p\_{\theta},p\_{r}) with a differentiable first-variation potential, which describes how redistributing probability mass changes 𝒟\mathcal{D}. Its spatial gradient specifies the field used in the sample update:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐠𝒟​(𝐱∣𝐜):=∇𝐱δ​𝒟​(pθ,pr)δ​pθ​(𝐱∣𝐜).\mathbf{g}\_{\mathcal{D}}(\mathbf{x}\mid\mathbf{c}):=\nabla\_{\mathbf{x}}\frac{\delta\mathcal{D}(p\_{\theta},p\_{r})}{\delta p\_{\theta}}(\mathbf{x}\mid\mathbf{c}). |  | (4) |

Under the assumptions in [Appendix B.1](#A2.SS1 "B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"),

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇θ𝒟​(pθ,pr)=𝔼𝐳∼pz​[[Jθ​Gθ​(𝐳,𝐜)]⊤⏟Jacobian transpose​𝐠𝒟​(Gθ​(𝐳,𝐜)∣𝐜)⏟distribution gradient].\nabla\_{\theta}\mathcal{D}(p\_{\theta},p\_{r})={\mathbb{E}}\_{\mathbf{z}\sim p\_{z}}\left[\underbrace{[J\_{\theta}G\_{\theta}(\mathbf{z},\mathbf{c})]^{\top}}\_{\text{Jacobian transpose}}\underbrace{\mathbf{g}\_{\mathcal{D}}(G\_{\theta}(\mathbf{z},\mathbf{c})\mid\mathbf{c})}\_{\text{distribution gradient}}\right]\,. |  | (5) |

Here Jθ​Gθ:=∂Gθ/∂θJ\_{\theta}G\_{\theta}:=\partial G\_{\theta}/\partial\theta; backpropagation applies its transpose, and training averages over 𝐜\mathbf{c}. For reverse KL, the first variation is log⁡(pθ/pr)+1\log(p\_{\theta}/p\_{r})+1, recovering Eq. [3](#S3.E3 "In 3.1 Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching"). Thus the score difference gives the distributional direction that is passed back through the generator. This separates the distributional change that reduces the discrepancy from the parameter update that realizes this change. The decomposition below concerns the former and does not depend on a particular generator architecture.

### 3.3 Decomposition of the Reverse-KL Field

To identify which statistics this field contains, let pp be a smooth positive density with finite second moment, mean μp\mu\_{p}, and positive-definite covariance Σp\Sigma\_{p}. Its moment-matched Gaussian is qp:=𝒩⁡(μp,Σp)q\_{p}:=\mathcal{N}(\mu\_{p},\Sigma\_{p}), with score 𝐬qp​(𝐱)=−Σp−1​(𝐱−μp)\mathbf{s}\_{q\_{p}}(\mathbf{x})=-\Sigma\_{p}^{-1}(\mathbf{x}-\mu\_{p}). The score of pp decomposes exactly as

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐬p​(𝐱)=𝐬qp​(𝐱)⏟=−Σp−1​(𝐱−μp)+𝜼p​(𝐱)⏟non-Gaussian score residual,\mathbf{s}\_{p}(\mathbf{x})=\underbrace{\mathbf{s}\_{q\_{p}}(\mathbf{x})}\_{=-\Sigma\_{p}^{-1}(\mathbf{x}-\mu\_{p})}+\underbrace{\bm{\eta}\_{p}(\mathbf{x})}\_{\text{non-Gaussian score residual}}\,, |  | (6) |

where 𝜼p:=𝐬p−𝐬qp\bm{\eta}\_{p}:=\mathbf{s}\_{p}-\mathbf{s}\_{q\_{p}} contains the score structure beyond this Gaussian approximation ([Wang and Vastola, 2023](#bib.bib79); [Wang and Vastola, 2024](#bib.bib80)).
At fixed 𝐜\mathbf{c}, use qi:=qpiq\_{i}:=q\_{p\_{i}} and 𝜼i:=𝜼pi\bm{\eta}\_{i}:=\bm{\eta}\_{p\_{i}} for the conditional laws pi(⋅∣𝐜)p\_{i}(\cdot\mid\mathbf{c}), i∈{r,θ}i\in\{r,\theta\}. Subtracting their decompositions gives

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐠KL(𝐱∣𝐜)=(𝐬qθ​(𝐱∣𝐜)−𝐬qr​(𝐱∣𝐜))⏟𝐠KLG:Gaussian moment component+(𝜼θ​(𝐱∣𝐜)−𝜼r​(𝐱∣𝐜))⏟𝐠KLnG:non-Gaussian residual component.\mathbf{g}\_{\mathrm{KL}}(\mathbf{x}\mid\mathbf{c})=\underbrace{\left(\mathbf{s}\_{q\_{\theta}}(\mathbf{x}\mid\mathbf{c})-\mathbf{s}\_{q\_{r}}(\mathbf{x}\mid\mathbf{c})\right)}\_{\mathbf{g}\_{\mathrm{KL}}^{\mathrm{G}}:\;\text{Gaussian moment component}}+\underbrace{\left(\bm{\eta}\_{\theta}(\mathbf{x}\mid\mathbf{c})-\bm{\eta}\_{r}(\mathbf{x}\mid\mathbf{c})\right)}\_{\mathbf{g}\_{\mathrm{KL}}^{\mathrm{nG}}:\;\text{non-Gaussian residual component}}. |  | (7) |

The Gaussian component depends only on means and covariances. Two distributions can share these moments yet have different shapes, leaving a nonzero residual in [Figure 3](#S3.F3 "Figure 3 ‣ 3.1 Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching"). Replacing pip\_{i} by pi,tp\_{i,t} gives the same decomposition for the noisy field used in DMD.

Under the integrability and boundary conditions in [Appendix B.2.2](#A2.SS2.SSS2 "B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"),

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝜼p​(𝐱)]=𝟎,𝔼p​[𝜼p​(𝐱)​𝐱⊤]=𝟎d×d.\mathbb{E}\_{p}[\bm{\eta}\_{p}(\mathbf{x})]=\mathbf{0},\qquad\mathbb{E}\_{p}[\bm{\eta}\_{p}(\mathbf{x})\mathbf{x}^{\top}]=\mathbf{0}\_{d\times d}. |  | (8) |

Each score residual is orthogonal to constant and linear functions under its own distribution; their difference need not be orthogonal under either distribution.
The moment-matched Gaussian is used to analyze the score; the generated samples are not assumed to follow a Gaussian distribution. The residual does not identify a single higher-order moment: it collects all score structure left after subtracting the Gaussian score for the corresponding distribution.

##### Implication for training.

Exact DMD already contains both components. In practice, its learned score estimates and finite training need not align all statistics accurately. The decomposition identifies moments as quantities that can be constrained explicitly, while the residual explains why moment matching alone is insufficient.
We therefore keep the full DMD correction and add a loss on feature means and standard deviations. Features from the generator’s EMA copy provide a shared representation without introducing an external encoder. This is an additional feature-space objective motivated by the decomposition, not a separate estimate of its sample-space Gaussian or residual component. The ablations in [Section 5.3](#S5.SS3 "5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching") test whether this explicit constraint improves generation.

## 4 Intrinsic Distribution Matching

Intrinsic Distribution Matching (IDM) retains internal DMD supervision and adds the feature-moment constraint motivated in [Section 3.3](#S3.SS3 "3.3 Decomposition of the Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching"). The DMD loss ℒscore\mathcal{L}\_{\text{score}} uses the full internal score-difference estimate; ℒpop\mathcal{L}\_{\text{pop}} explicitly matches statistics of generator EMA features. We first define how the DMD correction supervises velocity and endpoint predictions, then describe the feature constraint, the empirical moment estimates, and the gradients used in joint training.

### 4.1 DMD Loss

At a fixed condition 𝐜\mathbf{c}, let pr,tp\_{r,t} and pθ,tp\_{\theta,t} denote the reference and model marginals under the linear noising construction of [Section 2](#S2 "2 Background ‣ Intrinsic Distribution Matching"), with scores 𝐬r,t,𝐬θ,t\mathbf{s}\_{r,t},\mathbf{s}\_{\theta,t} and exact marginal velocities 𝐯r,t∗,𝐯θ,t∗\mathbf{v}^{\*}\_{r,t},\mathbf{v}^{\*}\_{\theta,t}.
Applying Eq. [1](#S2.E1 "In Score–Velocity Identity. ‣ 2 Background ‣ Intrinsic Distribution Matching") to both at the same point 𝐱t\mathbf{x}\_{t} gives, for t∈(0,1)t\in(0,1):

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐝t∗​(𝐱t):=𝐯θ,t∗​(𝐱t)−𝐯r,t∗​(𝐱t)=t1−t​(𝐬r,t​(𝐱t)−𝐬θ,t​(𝐱t)),\mathbf{d}\_{t}^{\*}(\mathbf{x}\_{t}):=\mathbf{v}^{\*}\_{\theta,t}(\mathbf{x}\_{t})-\mathbf{v}^{\*}\_{r,t}(\mathbf{x}\_{t})=\frac{t}{1{-}t}\left(\mathbf{s}\_{r,t}(\mathbf{x}\_{t})-\mathbf{s}\_{\theta,t}(\mathbf{x}\_{t})\right)\!, |  | (9) |

so 𝐠KL,t:=𝐬θ,t−𝐬r,t=−1−tt​𝐝t∗\mathbf{g}\_{\mathrm{KL},t}:=\mathbf{s}\_{\theta,t}-\mathbf{s}\_{r,t}=-\frac{1-t}{t}\,\mathbf{d}\_{t}^{\*} is the reverse-KL field on these noisy marginals in Eq. [3](#S3.E3 "In 3.1 Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching").

##### Internal velocity branches.

Following APEX ([Liu et al., 2026a](#bib.bib61)), we separate the reference and model velocity branches by negating the condition vector:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐯^r,t​(𝐱t∣𝐜):=𝑭θ​(𝐱t,t,𝐜),𝐯^θ,t​(𝐱t∣𝐜):=𝑭θ​(𝐱t,t,−𝐜),\widehat{\mathbf{v}}\_{r,t}(\mathbf{x}\_{t}\mid\mathbf{c}):=\bm{F}\_{\theta}(\mathbf{x}\_{t},t,\mathbf{c}),\qquad\widehat{\mathbf{v}}\_{\theta,t}(\mathbf{x}\_{t}\mid\mathbf{c}):=\bm{F}\_{\theta}(\mathbf{x}\_{t},t,-\mathbf{c}), |  | (10) |

Here −𝐜-\mathbf{c} selects the model branch for condition 𝐜\mathbf{c}, and 𝐝^t​(𝐱t∣𝐜):=𝐯^θ,t​(𝐱t∣𝐜)−𝐯^r,t​(𝐱t∣𝐜)\widehat{\mathbf{d}}\_{t}(\mathbf{x}\_{t}\mid\mathbf{c}):=\widehat{\mathbf{v}}\_{\theta,t}(\mathbf{x}\_{t}\mid\mathbf{c})-\widehat{\mathbf{v}}\_{r,t}(\mathbf{x}\_{t}\mid\mathbf{c}) is their pointwise difference.
This interpretation requires both branches to approximate their marginal velocities.

##### Velocity and endpoint regression.

The same DMD correction can supervise velocity predictions or their corresponding clean-sample endpoints. We compare these regression forms and their combinations in [Section 5.3](#S5.SS3 "5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching") to select the training configuration.

For fixed input 𝐱t\mathbf{x}\_{t} at time t∈(0,1]t\in(0,1], the endpoint prediction is 𝐱^0​(𝐱t,t,𝐜):=𝐱t−t​𝑭θ​(𝐱t,t,𝐜)\widehat{\mathbf{x}}\_{0}(\mathbf{x}\_{t},t,\mathbf{c}):=\mathbf{x}\_{t}-t\bm{F}\_{\theta}(\mathbf{x}\_{t},t,\mathbf{c}).
At t=1t=1 and 𝐱t=𝐳\mathbf{x}\_{t}=\mathbf{z}, this equals Gθ​(𝐳,𝐜)G\_{\theta}(\mathbf{z},\mathbf{c}); predictions at intermediate times need not follow the one-step output law pθp\_{\theta}.
Let sg\mathop{\operatorname{sg}}\nolimits denote stop-gradient. Set 𝐱^0sg:=sg(𝐱^0​(𝐱t,t,𝐜))\widehat{\mathbf{x}}\_{0}^{\mathop{\operatorname{sg}}\nolimits}:=\mathop{\operatorname{sg}}\nolimits(\widehat{\mathbf{x}}\_{0}(\mathbf{x}\_{t},t,\mathbf{c})) and re-noise it as 𝐱^0,t′sg:=(1−t′)​𝐱^0sg+t′​ϵ\widehat{\mathbf{x}}\_{0,t^{\prime}}^{\mathop{\operatorname{sg}}\nolimits}:=(1-t^{\prime})\widehat{\mathbf{x}}\_{0}^{\mathop{\operatorname{sg}}\nolimits}+t^{\prime}\bm{\epsilon}, where the re-noising time t′∈(0,1)t^{\prime}\in(0,1) and ϵ∼pz\bm{\epsilon}\sim p\_{z} are sampled independently of each other and of the regression input.
Evaluate the branch difference 𝐝^t′​(𝐱^0,t′sg∣𝐜)\widehat{\mathbf{d}}\_{t^{\prime}}(\widehat{\mathbf{x}}\_{0,t^{\prime}}^{\mathop{\operatorname{sg}}\nolimits}\mid\mathbf{c}) at this re-noised prediction. Its weighted, normalized value is detached to obtain 𝐝^t′DMD\widehat{\mathbf{d}}\_{t^{\prime}}^{\mathrm{DMD}}; without processing, the correction is sg(𝐝^t′​(𝐱^0,t′sg∣𝐜))\mathop{\operatorname{sg}}\nolimits\!\left(\widehat{\mathbf{d}}\_{t^{\prime}}(\widehat{\mathbf{x}}\_{0,t^{\prime}}^{\mathop{\operatorname{sg}}\nolimits}\mid\mathbf{c})\right).
The DMD targets are

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝐯tDMD\displaystyle\mathbf{v}\_{t}^{\mathrm{DMD}} | :=sg(𝑭θ​(𝐱t,t,𝐜)−𝐝^t′DMD),\displaystyle:=\mathop{\operatorname{sg}}\nolimits\!\left(\bm{F}\_{\theta}(\mathbf{x}\_{t},t,\mathbf{c})-\widehat{\mathbf{d}}\_{t^{\prime}}^{\mathrm{DMD}}\right), |  | (11) |
|  | 𝐱0DMD\displaystyle\mathbf{x}\_{0}^{\mathrm{DMD}} | :=sg(𝐱t−t​𝐯tDMD).\displaystyle:=\mathop{\operatorname{sg}}\nolimits\!\left(\mathbf{x}\_{t}-t\mathbf{v}\_{t}^{\mathrm{DMD}}\right). |  |

Subtracting this correction from the velocity target adds t​𝐝^t′DMDt\widehat{\mathbf{d}}\_{t^{\prime}}^{\mathrm{DMD}} to the detached clean-sample prediction. Thus the same correction defines both targets.
The combined squared regression loss, with both targets detached, averages over conditions, regression inputs and times, and re-noising draws:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒscore​(θ):=𝔼⁡[‖𝑭θ​(𝐱t,t,𝐜)−𝐯tDMD‖22⏟ℓv​(t)+‖𝐱^0​(𝐱t,t,𝐜)−𝐱0DMD‖22⏟ℓx​(t)].\mathcal{L}\_{\text{score}}(\theta):=\mathbb{E}\!\left[\underbrace{\|\bm{F}\_{\theta}(\mathbf{x}\_{t},t,\mathbf{c})-\mathbf{v}\_{t}^{\mathrm{DMD}}\|\_{2}^{2}}\_{\ell\_{v}(t)}+\underbrace{\|\widehat{\mathbf{x}}\_{0}(\mathbf{x}\_{t},t,\mathbf{c})-\mathbf{x}\_{0}^{\mathrm{DMD}}\|\_{2}^{2}}\_{\ell\_{x}(t)}\right]. |  | (12) |

At fixed (𝐱t,t)(\mathbf{x}\_{t},t), these squared losses satisfy ℓx​(t)=t2​ℓv​(t)\ell\_{x}(t)=t^{2}\ell\_{v}(t), so equal weights give an effective factor 1+t21+t^{2} on velocity regression in [Appendix B.4](#A2.SS4 "B.4 DMD Loss: Score-Difference Identity and Regression ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"). A separate discussion of conditional-mean regression and covariance appears in [Appendix B.7](#A2.SS7 "B.7 Covariance Contraction Under Regression ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").

Figure 4: 
Intrinsic losses of IDM.
Top, DMD loss: re-noise the predicted clean sample and use the internal velocity difference to construct detached velocity and endpoint targets for ℒscore\mathcal{L}\_{\text{score}} in Eq. [12](#S4.E12 "In Velocity and endpoint regression. ‣ 4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching").
Bottom, feature-moment loss: match means and per-coordinate standard deviations of EMA features 𝐡i:=ϕθ¯​(𝐱i,𝐜)\mathbf{h}\_{i}:=\phi\_{\bar{\theta}}(\mathbf{x}\_{i},\mathbf{c}) using current model features and detached model/reference queues 𝒬θ,𝒬r\mathcal{Q}\_{\theta},\mathcal{Q}\_{r} in Eq. [13](#S4.E13 "In Matching feature moments. ‣ 4.2 Feature-Moment Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching").
Base objective omitted.

### 4.2 Feature-Moment Loss

Alongside the learned DMD correction, we compare generated and reference samples in the feature space of the generator’s EMA copy. The EMA supplies the representation, while reference samples provide the target statistics for moment matching.

##### Intrinsic feature map.

ϕ:=ϕθ¯:ℝd×𝒞→ℝdϕ\phi:=\phi\_{\bar{\theta}}:\mathbb{R}^{d}\times\mathcal{C}\to\mathbb{R}^{d\_{\phi}} mean-pools the last-layer hidden activations of the generator’s EMA copy into one feature vector per sample. Generated and reference samples use the noising construction of [Section 2](#S2 "2 Background ‣ Intrinsic Distribution Matching") at high noise levels, with noising arguments suppressed in ϕ\phi. Here θ¯\bar{\theta} denotes EMA parameters and dϕd\_{\phi} the feature dimension; each update fixes θ¯\bar{\theta} while retaining input derivatives.
We compare this choice with frozen-encoder ([Yang et al., 2026](#bib.bib65)), teacher-feature ([Zhang et al., 2026b](#bib.bib67)), and live self-feature alternatives in [Section 5.3](#S5.SS3 "5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching").

##### Matching feature moments.

Let μiϕ\mu\_{i}^{\phi} and νi,jϕ\nu\_{i,j}^{\phi} denote the mean and per-coordinate variance of ϕ⁡(𝐱,𝐜)\phi(\mathbf{x},\mathbf{c}) under the joint law (𝐱,𝐜)∼pi(⋅∣𝐜)pc(\mathbf{x},\mathbf{c})\sim p\_{i}(\cdot\mid\mathbf{c})p\_{c}, also averaging over feature-extraction noise, for i∈{r,θ}i\in\{r,\theta\}. These statistics pool across conditions rather than matching conditional distributions.
We match these pooled statistics with

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒpop=‖μθϕ−μrϕ‖22+∑j=1dϕ(νθ,jϕ−νr,jϕ)2.\mathcal{L}\_{\text{pop}}=\|\mu\_{\theta}^{\phi}-\mu\_{r}^{\phi}\|\_{2}^{2}+\sum\_{j=1}^{d\_{\phi}}\left(\sqrt{\nu\_{\theta,j}^{\phi}}-\sqrt{\nu\_{r,j}^{\phi}}\right)^{2}\!. |  | (13) |

This is the squared 2-Wasserstein distance between the diagonal Gaussians 𝒩⁡(μiϕ,diag(νiϕ))\mathcal{N}(\mu\_{i}^{\phi},\diag(\nu\_{i}^{\phi})); it is non-negative and vanishes exactly when their feature means and per-coordinate standard deviations match. At the feature level, the mean term shifts the average toward the reference mean, while the standard-deviation term adjusts the spread around that average. These roles are explicit in the empirical gradient in [Prop. B.20](#A2.Thmtheorem20 "Proposition B.20 (Gradient of the Feature-Moment Loss) . ‣ Fixed-feature updates. ‣ B.6 Gradient of the Feature-Moment Loss ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"). Their effect on images is mediated by the fixed EMA feature Jacobian and the generator, so the objective does not prescribe a pixel-wise correction.
A nonlinear feature map can capture properties not determined by raw-sample means and covariances. Matching its moments therefore constrains statistics in a learned representation. The loss still uses only pooled feature means and per-coordinate standard deviations; it does not estimate the sample-space Gaussian component or match the full feature distribution.

Queues 𝒬θ\mathcal{Q}\_{\theta} and 𝒬r\mathcal{Q}\_{r} store up to K=16384K=16384 detached model and reference features, respectively. Model moments combine BB current-batch features with 𝒬θ\mathcal{Q}\_{\theta}; reference moments use 𝒬r\mathcal{Q}\_{r}, giving B+KB+K and KK features with full queues. These moments define ℒ^pop\widehat{\mathcal{L}}\_{\text{pop}}.
Queue entries come from earlier model and EMA states, so the moments approximate current population statistics. [Prop. B.20](#A2.Thmtheorem20 "Proposition B.20 (Gradient of the Feature-Moment Loss) . ‣ Fixed-feature updates. ‣ B.6 Gradient of the Feature-Moment Loss ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching") gives the exact empirical-loss gradient at fixed queues in [Appendix B.6](#A2.SS6 "B.6 Gradient of the Feature-Moment Loss ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").

### 4.3 Training Objective

We use the RCGM loss ([Sun and Lin, 2025](#bib.bib59)), which supervises generation across time intervals through recursive consistent velocity-field estimation, as ℒbase\mathcal{L}\_{\text{base}}. The main generator objective is

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒIDM ​(θ)=ℒbase​(θ)+λscore​ℒscore​(θ)+λpop​ℒ^pop.\mathcal{L}\_{\text{{IDM} }}(\theta)=\mathcal{L}\_{\text{base}}(\theta)+\lambda\_{\text{score}}\mathcal{L}\_{\text{score}}(\theta)+\lambda\_{\text{pop}}\widehat{\mathcal{L}}\_{\text{pop}}. |  | (14) |

Each iteration generates current samples and extracts their high-noise EMA features. The current features retain their computation graph and are combined with the detached queues to evaluate ℒ^pop\widehat{\mathcal{L}}\_{\text{pop}}. Its gradient passes through the fixed EMA network to the current samples and generator; queued features receive no gradients. Across iterations, we refresh the queues with detached features and update the EMA as θ¯←0.99​θ¯+0.01​θ\bar{\theta}\leftarrow 0.99\bar{\theta}+0.01\theta. The weights λscore\lambda\_{\text{score}} and λpop\lambda\_{\text{pop}} remain fixed in [Section 5.1](#S5.SS1 "5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching"). Feature extraction and queues are used only during training.
Freezing the EMA parameters does not freeze the current features: their values change with the generated images. Detaching these features would also remove the moment-loss gradient to the generator. The detached queues provide historical statistics without retaining computation graphs from previous iterations.
Auxiliary flow matching ℒfake\mathcal{L}\_{\text{fake}} trains the internal model-velocity branch on detached generated samples and also updates the shared parameters in [Appendix B.5](#A2.SS5 "B.5 Internal model-velocity training ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
One-step inference generates 𝐱θ=Gθ​(𝐳,𝐜)\mathbf{x}\_{\theta}=G\_{\theta}(\mathbf{z},\mathbf{c}) in one forward pass; the same checkpoint also supports few-step sampling.

## 5 Experiments

Our experiments assess the added value of ℒpop\mathcal{L}\_{\text{pop}} over internal DMD, the suitability of generator EMA features relative to an external encoder, and the choice of velocity and endpoint regression. System-level comparisons evaluate the complete training setting; controlled ablations examine these individual choices under the shared data, backbone, and sampling budget. Throughout this section, ℒpop\mathcal{L}\_{\text{pop}} refers to the empirical loss ℒ^pop\widehat{\mathcal{L}}\_{\text{pop}}.

Table 1: System-level comparison of efficiency and quality.
Speeds are on a single A100 (BF16).
Throughput is samples/s (batch=10); latency is seconds (batch=1).
GenEval measures compositional prompt following; FID/CLIP complement the efficiency comparison. LongText results appear in [Table 5](#S5.T5 "Table 5 ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
† indicates that distinct models are required for different NFEs.
‡ marks a noncanonical operating point or a secondary comparison source.
§ indicates that the LoRA weights are merged into the base weights before timing.
Params: backbone size in billions; LoRA entries additionally give rank rr and trainable parameters in parentheses. Blue/red backbone counts indicate full/LoRA tuning, respectively.

|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Methods | | NFEs | Throughput | Latency | Params | FID ↓\downarrow | CLIP ↑\uparrow | GenEval ↑\uparrow |
| (samples/s) | (s) | (B) |
| Few-Step Generative Models | SDXL-LCM [Luo et al. (2023)](#bib.bib21) | 2 | 2.89 | 0.40 | 0.9 | 18.11 | 27.51 | 0.44 |
| PixArt-LCM [Chen et al. (2024c)](#bib.bib22) | 2 | 3.52 | 0.31 | 0.6 | 10.33 | 27.24 | 0.42 |
| SD3.5-Turbo ([Esser et al., 2024](#bib.bib1))‡ | 2 | 1.61 | 0.68 | 8.0 | 51.47 | 25.59 | 0.53 |
| PCM [Wang et al. (2024a)](#bib.bib20)† | 2 | 2.62 | 0.56 | 0.9 | 14.70 | 27.66 | 0.55 |
| SDXL-DMD2 [Yin et al. (2024a)](#bib.bib14)† | 2 | 2.89 | 0.40 | 0.9 | 7.61 | 28.87 | 0.58 |
| FLUX-schnell ([Labs, 2024](#bib.bib18)) | 2 | 0.92 | 1.15 | 12.0 | 7.75 | 28.25 | 0.71 |
| Sana-Sprint ([Chen et al., 2025b](#bib.bib15)) | 2 | 6.46 | 0.25 | 0.6 | 6.54 | 28.40 | 0.76 |
| Sana-Sprint ([Chen et al., 2025b](#bib.bib15)) | 2 | 5.68 | 0.24 | 1.6 | 6.50 | 28.45 | 0.77 |
| Qwen-Image-Lightning ([ModelTC, 2025](#bib.bib38))‡ | 2 | 3.15 | 0.48 | 20.0 (r=64,0.4)§ | 6.76 | 28.37 | 0.85 |
| TwinFlow (Qwen-Image) ([Cheng et al., 2025](#bib.bib56)) | 2 | 3.15 | 0.48 | 20.0 (r=64,0.4)§ | – | – | 0.87 |
| APEX (Qwen-Image) ([Liu et al., 2026a](#bib.bib61)) | 2 | 3.21 | 0.49 | 20.0 (r=32,0.2)§ | 6.72 | 28.71 | 0.87 |
| APEX (Qwen-Image) ([Liu et al., 2026a](#bib.bib61)) | 2 | 3.17 | 0.47 | 20.0 (r=64,0.4)§ | 6.51 | 28.42 | 0.89 |
| APEX (Qwen-Image) ([Liu et al., 2026a](#bib.bib61)) | 2 | 3.30 | 0.45 | 20.0 | 6.44 | 28.51 | 0.90 |
| IDM (Z-Image) | 2 | 5.18 | 0.30 | 6.0 (r=32,0.2)§ | 6.98 | 28.41 | 0.76 |
| IDM (Z-Image) | 2 | 5.18 | 0.30 | 6.0 (r=64,0.4)§ | 6.79 | 28.13 | 0.77 |
| IDM (Z-Image) | 2 | 5.18 | 0.30 | 6.0 | 6.71 | 28.22 | 0.78 |
| IDM (Qwen-Image) | 2 | 3.28 | 0.44 | 20.0 (r=32,0.2)§ | 6.62 | 28.76 | 0.89 |
| IDM (Qwen-Image) | 2 | 3.28 | 0.44 | 20.0 (r=64,0.4)§ | 6.41 | 28.47 | 0.90 |
| IDM (Qwen-Image) | 2 | 3.28 | 0.44 | 20.0 | 6.34 | 28.56 | 0.91 |
| SDXL-LCM [Luo et al. (2023)](#bib.bib21) | 1 | 3.36 | 0.32 | 0.9 | 50.51 | 24.45 | 0.28 |
| PixArt-LCM [Chen et al. (2024c)](#bib.bib22) | 1 | 4.26 | 0.25 | 0.6 | 73.35 | 23.99 | 0.41 |
| PixArt-DMD ([Chen et al., 2024b](#bib.bib19); [Yin et al., 2024b](#bib.bib16))† | 1 | 4.26 | 0.25 | 0.6 | 9.59 | 26.98 | 0.45 |
| SD3.5-Turbo ([Esser et al., 2024](#bib.bib1))‡ | 1 | 2.48 | 0.45 | 8.0 | 52.40 | 25.40 | 0.51 |
| PCM [Wang et al. (2024a)](#bib.bib20)† | 1 | 3.16 | 0.40 | 0.9 | 30.11 | 26.47 | 0.42 |
| SDXL-DMD2 [Yin et al. (2024a)](#bib.bib14)† | 1 | 3.36 | 0.32 | 0.9 | 7.10 | 28.93 | 0.59 |
| FLUX-schnell ([Labs, 2024](#bib.bib18)) | 1 | 1.58 | 0.68 | 12.0 | 7.26 | 28.49 | 0.69 |
| Sana-Sprint ([Chen et al., 2025b](#bib.bib15)) | 1 | 7.22 | 0.21 | 0.6 | 7.04 | 28.04 | 0.72 |
| Sana-Sprint ([Chen et al., 2025b](#bib.bib15)) | 1 | 6.71 | 0.21 | 1.6 | 7.69 | 28.27 | 0.76 |
| Qwen-Image-Lightning ([ModelTC, 2025](#bib.bib38))‡ | 1 | 3.29 | 0.40 | 20.0 (r=64,0.4)§ | 7.06 | 28.35 | 0.85 |
| TwinFlow (Qwen-Image) ([Cheng et al., 2025](#bib.bib56)) | 1 | 3.29 | 0.40 | 20.0 (r=64,0.4)§ | – | – | 0.86 |
| APEX (Qwen-Image) ([Liu et al., 2026a](#bib.bib61)) | 1 | 3.29 | 0.39 | 20.0 (r=32,0.2)§ | 7.22 | 28.62 | 0.88 |
| APEX (Qwen-Image) ([Liu et al., 2026a](#bib.bib61)) | 1 | 3.27 | 0.39 | 20.0 (r=64,0.4)§ | 7.14 | 28.45 | 0.89 |
| APEX (Qwen-Image) ([Liu et al., 2026a](#bib.bib61)) | 1 | 3.50 | 0.34 | 20.0 | 6.87 | 28.66 | 0.89 |
| IDM (Z-Image) | 1 | 5.41 | 0.25 | 6.0 (r=32,0.2)§ | 7.49 | 28.33 | 0.75 |
| IDM (Z-Image) | 1 | 5.41 | 0.25 | 6.0 (r=64,0.4)§ | 7.40 | 28.16 | 0.76 |
| IDM (Z-Image) | 1 | 5.41 | 0.25 | 6.0 | 7.13 | 28.37 | 0.77 |
| IDM (Qwen-Image) | 1 | 3.44 | 0.35 | 20.0 (r=32,0.2)§ | 7.12 | 28.67 | 0.88 |
| IDM (Qwen-Image) | 1 | 3.44 | 0.35 | 20.0 (r=64,0.4)§ | 7.04 | 28.50 | 0.89 |
| IDM (Qwen-Image) | 1 | 3.44 | 0.35 | 20.0 | 6.77 | 28.71 | 0.90 |

### 5.1 Experimental Setup

##### Backbones and tuning.

We initialize IDM from Z-Image-Turbo 6B ([Team, 2025](#bib.bib49)) and Qwen-Image 20B ([Wu et al., 2025a](#bib.bib33)), using full-parameter tuning and LoRA with ranks 32 and 64. We denote the resulting models by IDM (Z-Image) and IDM (Qwen-Image); the former uses the Turbo checkpoint rather than the undistilled Z-Image base model.

##### Training data.

The reference data defining prp\_{r} combine ShareGPT-4o ([Chen et al., 2025c](#bib.bib41)), BLIP-3o ([Chen et al., 2025a](#bib.bib40)), and samples synthesized with Qwen-Image-2512 and Z-Image-Turbo: 600K from FLUX-Reason-6M prompts ([Fang et al., 2025](#bib.bib48)) and 5M from text-rendering prompts. Compared with the 200K poster-prompt samples used by APEX ([Liu et al., 2026a](#bib.bib61)), this larger text-focused collection provides more training examples for dense text rendering.

##### Training configuration.

All models use BF16, FlashAttention4, and FSDP2 with global batch size 64.
Training runs for 15K steps on Z-Image-Turbo 6B and 10K steps for Qwen-Image 20B LoRA, using 32×\timesH100 80GB and 8×\timesA100 80GB GPUs.
The default weights are λscore=1\lambda\_{\text{score}}=1 and λpop=0.5\lambda\_{\text{pop}}=0.5, fixed throughout training.
Each trained checkpoint is evaluated at both 1 and 2 NFE without changing the training loss weights for either sampling budget.

##### Evaluation.

We follow the same standard benchmark protocols used for the APEX comparisons, reporting each method at its stated NFE budget. Published reference results retain their training data and configuration; the internal IDM ablations use the shared configuration above.
We evaluate compositional prompt following with GenEval ([Ghosh et al., 2023](#bib.bib36)), FID and CLIP score on MJHQ-30K ([Li et al., 2024a](#bib.bib35)), detailed prompt following on DPG-Bench ([Hu et al., 2024](#bib.bib37)), and world knowledge on WISE ([Niu et al., 2025](#bib.bib45)).
Z-Image comparisons and ablations additionally report OneIG ([Chang et al., 2026](#bib.bib82)) and LongText-Bench ([Geng et al., 2025b](#bib.bib83)); LongText-CN and LongText-EN measure Chinese and English long-text rendering, respectively.

### 5.2 Main Comparison

##### Long-text rendering.

At 2 NFE, IDM (Z-Image) achieves 94.25% on LongText-CN and 90.20% on LongText-EN, the highest scores among the compared methods at this budget in [Table 5](#S5.T5 "Table 5 ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching"). These improve over Z-Image-Turbo++ by 2.63 and 0.32 percentage points and over APEX by 3.87 and 1.44 points, respectively. This directly supports the fine-grained text-rendering objective introduced above. The table places external comparisons alongside the controlled ablations, allowing the contribution of each loss to be examined.

##### General quality and efficiency.

With full-parameter tuning, IDM achieves GenEval scores of 0.78 on Z-Image and 0.91 on Qwen-Image at 2 NFE in [Table 1](#S5.T1 "Table 1 ‣ 5 Experiments ‣ Intrinsic Distribution Matching"). On Qwen-Image under the same NFE and tuning setting, APEX scores 0.90; FID is 6.34 for IDM and 6.44 for APEX, with latencies of 0.44 and 0.45 seconds. Thus, the quality improvement comes at comparable sampling latency. At 1 NFE, Qwen-Image IDM reaches 0.90 GenEval at 0.35 seconds per sample, giving a faster sampling option with the same trained checkpoint.

The same full-parameter checkpoints improve from 1 to 2 NFE on both backbones: Z-Image FID decreases from 7.13 to 6.71 and Qwen-Image FID from 6.77 to 6.34, while each gains 0.01 GenEval. Thus the learned objectives remain useful when the sampling budget allows an additional network evaluation.
With rank-64 LoRA, Qwen-Image IDM trains 0.4B parameters and reaches 0.90 GenEval at 2 NFE, compared with 0.91 under full tuning. This setting retains most of the compositional performance while updating substantially fewer parameters. DPG-Bench and WISE provide complementary evaluations of prompt following and world knowledge. Figure [6](#S5.F6 "Figure 6 ‣ Qualitative comparison. ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching") presents qualitative comparisons across sampling budgets.

[Table 2](#S5.T2 "Table 2 ‣ General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"), [Table 3](#S5.T3 "Table 3 ‣ General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"), and [Table 4](#S5.T4 "Table 4 ‣ General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching") provide the per-category results for GenEval, WISE, and DPG-Bench.

Table 2: Quantitative evaluation on GenEval. Per-category and overall scores at the NFE shown in each model label; unlabeled published baselines use their reported default sampling budget. Z-Image is the base model (∼\sim100 NFE), whereas Z-Image-Turbo is the 8-NFE distilled model.

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Model | Single | Two | Counting | Colors | Position | Attribute | Overall↑\uparrow |
| Object | Object | Binding |
| Show-o ([Xie et al., 2024](#bib.bib23)) | 0.95 | 0.52 | 0.49 | 0.82 | 0.11 | 0.28 | 0.53 |
| Emu3-Gen ([Wang et al., 2024b](#bib.bib24)) | 0.98 | 0.71 | 0.34 | 0.81 | 0.17 | 0.21 | 0.54 |
| PixArt-α\alpha ([Chen et al., 2024d](#bib.bib25)) | 0.98 | 0.50 | 0.44 | 0.80 | 0.08 | 0.07 | 0.48 |
| SD3 Medium ([Esser et al., 2024](#bib.bib1)) | 0.98 | 0.74 | 0.63 | 0.67 | 0.34 | 0.36 | 0.62 |
| FLUX.1 [Dev] ([BlackForest, 2024](#bib.bib26)) | 0.98 | 0.81 | 0.74 | 0.79 | 0.22 | 0.45 | 0.66 |
| SD3.5 Large ([Esser et al., 2024](#bib.bib1))‡ | 0.98 | 0.89 | 0.73 | 0.83 | 0.34 | 0.47 | 0.71 |
| JanusFlow ([Ma et al., 2025](#bib.bib27)) | 0.97 | 0.59 | 0.45 | 0.83 | 0.53 | 0.42 | 0.63 |
| Lumina-Image 2.0 ([Qin et al., 2025](#bib.bib28)) | - | 0.87 | 0.67 | - | - | 0.62 | 0.73 |
| Janus-Pro-7B ([Chen et al., 2025d](#bib.bib29)) | 0.99 | 0.89 | 0.59 | 0.90 | 0.79 | 0.66 | 0.80 |
| HiDream-I1-Full ([Cai et al., 2025](#bib.bib30)) | 1.00 | 0.98 | 0.79 | 0.91 | 0.60 | 0.72 | 0.83 |
| GPT Image 1 [High] ([OpenAI, 2025](#bib.bib31)) | 0.99 | 0.92 | 0.85 | 0.92 | 0.75 | 0.61 | 0.84 |
| Seedream 3.0 ([Gao et al., 2025](#bib.bib32)) | 0.99 | 0.96 | 0.91 | 0.93 | 0.47 | 0.80 | 0.84 |
| BAGEL ([Deng et al., 2025](#bib.bib44)) | 0.98 | 0.95 | 0.84 | 0.95 | 0.78 | 0.77 | 0.88 |
| Qwen-Image ([Wu et al., 2025a](#bib.bib33)) | 0.99 | 0.92 | 0.89 | 0.88 | 0.76 | 0.77 | 0.87 |
| Hyper-BAGEL ([Lu et al., 2025](#bib.bib43)) | 0.97 | 0.86 | 0.75 | 0.90 | 0.67 | 0.62 | 0.80 |
| Qwen-Image-Lightning ([ModelTC, 2025](#bib.bib38); [Liu et al., 2026a](#bib.bib61))‡ | 0.99 | 0.89 | 0.85 | 0.87 | 0.75 | 0.76 | 0.85 |
| Z-Image ([Team, 2025](#bib.bib49)) (base; ∼\sim100 NFE) | 1.00 | 0.94 | 0.78 | 0.93 | 0.62 | 0.77 | 0.84 |
| Z-Image-Turbo ([Team, 2025](#bib.bib49); [Liu et al., 2026b](#bib.bib50)) | 1.00 | 0.89 | 0.72 | 0.85 | 0.46 | 0.59 | 0.75 |
| DMD2 ([Yin et al., 2024a](#bib.bib14); [Liu et al., 2026b](#bib.bib50)) (2 NFE) | 1.00 | 0.90 | 0.68 | 0.84 | 0.49 | 0.66 | 0.76 |
| TwinFlow ([Cheng et al., 2025](#bib.bib56); [Liu et al., 2026b](#bib.bib50)) (2 NFE) | 1.00 | 0.87 | 0.68 | 0.85 | 0.40 | 0.55 | 0.72 |
| Z-Image-Turbo++ ([Liu et al., 2026b](#bib.bib50)) (2 NFE) | 1.00 | 0.88 | 0.69 | 0.85 | 0.49 | 0.65 | 0.76 |
| TwinFlow (Qwen-Image) ([Cheng et al., 2025](#bib.bib56)) (1 NFE) | 1.00 | 0.91 | 0.84 | 0.90 | 0.75 | 0.74 | 0.86 |
| APEX (Qwen-Image) (LoRA&r=32) (1 NFE) | 0.99 | 0.95 | 0.85 | 0.90 | 0.79 | 0.78 | 0.88 |
| APEX (Qwen-Image) (LoRA&r=64) (1 NFE) | 0.99 | 0.94 | 0.88 | 0.90 | 0.85 | 0.78 | 0.89 |
| APEX (Qwen-Image) (Full) (1 NFE) | 0.99 | 0.92 | 0.83 | 0.91 | 0.86 | 0.81 | 0.89 |
| IDM (Z-Image) (LoRA&r=32) (2 NFE) | 1.00 | 0.90 | 0.69 | 0.87 | 0.47 | 0.62 | 0.76 |
| IDM (Z-Image) (LoRA&r=64) (2 NFE) | 1.00 | 0.90 | 0.70 | 0.87 | 0.49 | 0.64 | 0.77 |
| IDM (Z-Image) (Full) (2 NFE) | 1.00 | 0.91 | 0.71 | 0.88 | 0.51 | 0.66 | 0.78 |
| IDM (Z-Image) (LoRA&r=32) (1 NFE) | 1.00 | 0.89 | 0.68 | 0.86 | 0.45 | 0.61 | 0.75 |
| IDM (Z-Image) (LoRA&r=64) (1 NFE) | 1.00 | 0.90 | 0.69 | 0.87 | 0.47 | 0.63 | 0.76 |
| IDM (Z-Image) (Full) (1 NFE) | 1.00 | 0.90 | 0.70 | 0.87 | 0.49 | 0.64 | 0.77 |
| IDM (Qwen-Image) (LoRA&r=32) (2 NFE) | 1.00 | 0.95 | 0.87 | 0.92 | 0.79 | 0.83 | 0.89 |
| IDM (Qwen-Image) (LoRA&r=64) (2 NFE) | 1.00 | 0.95 | 0.88 | 0.92 | 0.81 | 0.84 | 0.90 |
| IDM (Qwen-Image) (Full) (2 NFE) | 1.00 | 0.96 | 0.89 | 0.93 | 0.83 | 0.86 | 0.91 |
| IDM (Qwen-Image) (LoRA&r=32) (1 NFE) | 1.00 | 0.94 | 0.86 | 0.91 | 0.77 | 0.81 | 0.88 |
| IDM (Qwen-Image) (LoRA&r=64) (1 NFE) | 1.00 | 0.95 | 0.87 | 0.92 | 0.79 | 0.83 | 0.89 |
| IDM (Qwen-Image) (Full) (1 NFE) | 1.00 | 0.95 | 0.88 | 0.92 | 0.81 | 0.84 | 0.90 |

Table 3: Quantitative evaluation on WISE ([Niu et al., 2025](#bib.bib45)). Per-domain and overall world-knowledge grounding scores.

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Model | Cultural | Time | Space | Biology | Physics | Chemistry | Overall↑\uparrow |
| SD v1.5 ([Rombach et al., 2022](#bib.bib3)) | 0.34 | 0.35 | 0.32 | 0.28 | 0.29 | 0.21 | 0.32 |
| SDXL ([Podell et al., 2023](#bib.bib2)) | 0.43 | 0.48 | 0.47 | 0.44 | 0.45 | 0.27 | 0.43 |
| SD3.5-Large ([Esser et al., 2024](#bib.bib1))‡ | 0.44 | 0.50 | 0.58 | 0.44 | 0.52 | 0.31 | 0.46 |
| PixArt-α\alpha ([Chen et al., 2024d](#bib.bib25)) | 0.45 | 0.50 | 0.48 | 0.49 | 0.56 | 0.34 | 0.47 |
| Playground-v2.5 ([Li et al., 2024a](#bib.bib35)) | 0.49 | 0.58 | 0.55 | 0.43 | 0.48 | 0.33 | 0.49 |
| FLUX.1 [Dev] ([BlackForest, 2024](#bib.bib26)) | 0.48 | 0.58 | 0.62 | 0.42 | 0.51 | 0.35 | 0.50 |
| Janus ([Wu et al., 2025b](#bib.bib39)) | 0.16 | 0.26 | 0.35 | 0.28 | 0.30 | 0.14 | 0.23 |
| VILA-u-7B-256 ([Wu et al., 2024](#bib.bib47)) | 0.26 | 0.33 | 0.37 | 0.35 | 0.39 | 0.23 | 0.31 |
| Show-o ([Xie et al., 2024](#bib.bib23)) | 0.28 | 0.40 | 0.48 | 0.30 | 0.46 | 0.30 | 0.35 |
| Janus-Pro-7B ([Chen et al., 2025d](#bib.bib29)) | 0.30 | 0.37 | 0.49 | 0.36 | 0.42 | 0.26 | 0.35 |
| Emu3-Gen ([Wang et al., 2024b](#bib.bib24)) | 0.34 | 0.45 | 0.48 | 0.41 | 0.45 | 0.27 | 0.39 |
| MetaQuery-XL ([Pan et al., 2025](#bib.bib46)) | 0.56 | 0.55 | 0.62 | 0.49 | 0.63 | 0.41 | 0.55 |
| BAGEL ([Deng et al., 2025](#bib.bib44)) | 0.44 | 0.55 | 0.68 | 0.44 | 0.60 | 0.39 | 0.52 |
| GPT-Image-1 ([OpenAI, 2025](#bib.bib31)) | 0.81 | 0.71 | 0.89 | 0.83 | 0.79 | 0.74 | 0.80 |
| TwinFlow (Qwen-Image; 1 NFE) ([Cheng et al., 2025](#bib.bib56)) | – | – | – | – | – | – | 0.54 |
| APEX (Qwen-Image) (LoRA&r=32) (1 NFE) | – | – | – | – | – | – | – |
| APEX (Qwen-Image) (LoRA&r=64) (1 NFE) | – | – | – | – | – | – | – |
| APEX (Qwen-Image) (Full) (1 NFE) | 0.53 | 0.54 | 0.66 | 0.48 | 0.61 | 0.41 | 0.54 |
| IDM (Z-Image) (LoRA&r=32) (2 NFE) | 0.45 | 0.46 | 0.56 | 0.41 | 0.52 | 0.37 | 0.46 |
| IDM (Z-Image) (LoRA&r=64) (2 NFE) | 0.46 | 0.47 | 0.58 | 0.42 | 0.54 | 0.37 | 0.47 |
| IDM (Z-Image) (Full) (2 NFE) | 0.47 | 0.48 | 0.59 | 0.43 | 0.55 | 0.38 | 0.48 |
| IDM (Z-Image) (LoRA&r=32) (1 NFE) | 0.43 | 0.44 | 0.55 | 0.40 | 0.51 | 0.36 | 0.45 |
| IDM (Z-Image) (LoRA&r=64) (1 NFE) | 0.44 | 0.45 | 0.56 | 0.41 | 0.52 | 0.36 | 0.46 |
| IDM (Z-Image) (Full) (1 NFE) | 0.46 | 0.47 | 0.58 | 0.42 | 0.54 | 0.37 | 0.47 |
| IDM (Qwen-Image) (LoRA&r=32) (2 NFE) | 0.53 | 0.54 | 0.65 | 0.48 | 0.60 | 0.41 | 0.54 |
| IDM (Qwen-Image) (LoRA&r=64) (2 NFE) | 0.54 | 0.55 | 0.67 | 0.49 | 0.62 | 0.41 | 0.55 |
| IDM (Qwen-Image) (Full) (2 NFE) | 0.55 | 0.56 | 0.68 | 0.50 | 0.63 | 0.42 | 0.56 |
| IDM (Qwen-Image) (LoRA&r=32) (1 NFE) | 0.51 | 0.52 | 0.64 | 0.47 | 0.59 | 0.40 | 0.52 |
| IDM (Qwen-Image) (LoRA&r=64) (1 NFE) | 0.53 | 0.54 | 0.65 | 0.48 | 0.60 | 0.41 | 0.54 |
| IDM (Qwen-Image) (Full) (1 NFE) | 0.54 | 0.55 | 0.67 | 0.49 | 0.62 | 0.41 | 0.55 |

Table 4: Quantitative evaluation on DPG-Bench. NFE notation follows [Table 2](#S5.T2 "Table 2 ‣ General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Model | Global | Entity | Attribute | Relation | Other | Overall↑\uparrow |
| SD v1.5 ([Rombach et al., 2022](#bib.bib3)) | 74.63 | 74.23 | 75.39 | 73.49 | 67.81 | 63.18 |
| PixArt-α\alpha ([Chen et al., 2024d](#bib.bib25)) | 74.97 | 79.32 | 78.60 | 82.57 | 76.96 | 71.11 |
| Lumina-Next ([Zhuo et al., 2024](#bib.bib42)) | 82.82 | 88.65 | 86.44 | 80.53 | 81.82 | 74.63 |
| SDXL ([Podell et al., 2023](#bib.bib2)) | 83.27 | 82.43 | 80.91 | 86.76 | 80.41 | 74.65 |
| Hunyuan-DiT ([Li et al., 2024b](#bib.bib34)) | 84.59 | 80.59 | 88.01 | 74.36 | 86.41 | 78.87 |
| Janus ([Wu et al., 2025b](#bib.bib39)) | 82.33 | 87.38 | 87.70 | 85.46 | 86.41 | 79.68 |
| PixArt-Σ\Sigma ([Chen et al., 2024a](#bib.bib8)) | 86.89 | 82.89 | 88.94 | 86.59 | 87.68 | 80.54 |
| Emu3-Gen ([Wang et al., 2024b](#bib.bib24)) | 85.21 | 86.68 | 86.84 | 90.22 | 83.15 | 80.60 |
| Janus-Pro-1B ([Chen et al., 2025d](#bib.bib29)) | 87.58 | 88.63 | 88.17 | 88.98 | 88.30 | 82.63 |
| DALL-E 3 ([OpenAI, 2023](#bib.bib17)) | 90.97 | 89.61 | 88.39 | 90.58 | 89.83 | 83.50 |
| FLUX.1 [Dev] ([BlackForest, 2024](#bib.bib26)) | 74.35 | 90.00 | 88.96 | 90.87 | 88.33 | 83.84 |
| SD3 Medium ([Esser et al., 2024](#bib.bib1)) | 87.90 | 91.01 | 88.83 | 80.70 | 88.68 | 84.08 |
| SD3.5-Turbo ([Esser et al., 2024](#bib.bib1))‡ | 79.03 | 80.12 | 86.13 | 84.73 | 91.86 | 78.29 |
| SD3.5-Large ([Esser et al., 2024](#bib.bib1))‡ | 83.21 | 84.27 | 88.99 | 87.35 | 93.28 | 80.35 |
| FLUX.1-schnell [Labs (2024)](#bib.bib18) | 84.94 | 86.62 | 90.82 | 88.35 | 93.45 | 82.00 |
| Janus-Pro-7B ([Chen et al., 2025d](#bib.bib29)) | 86.90 | 88.90 | 89.40 | 89.32 | 89.48 | 84.19 |
| HiDream-I1-Full ([Cai et al., 2025](#bib.bib30)) | 76.44 | 90.22 | 89.48 | 93.74 | 91.83 | 85.89 |
| Lumina-Image 2.0 ([Qin et al., 2025](#bib.bib28)) | - | 91.97 | 90.20 | 94.85 | - | 87.20 |
| Seedream 3.0 ([Gao et al., 2025](#bib.bib32)) | 94.31 | 92.65 | 91.36 | 92.78 | 88.24 | 88.27 |
| GPT Image 1 [High] ([OpenAI, 2025](#bib.bib31)) | 88.89 | 88.94 | 89.84 | 92.63 | 90.96 | 85.15 |
| Qwen-Image ([Wu et al., 2025a](#bib.bib33)) | 91.32 | 91.56 | 92.02 | 94.31 | 92.73 | 88.32 |
| Z-Image ([Team, 2025](#bib.bib49)) (base; ∼\sim100 NFE) | 93.39 | 91.22 | 93.16 | 92.22 | 91.52 | 88.14 |
| Z-Image-Turbo ([Team, 2025](#bib.bib49); [Liu et al., 2026b](#bib.bib50)) | 91.29 | 89.59 | 90.14 | 92.16 | 88.68 | 84.86 |
| DMD2 ([Yin et al., 2024a](#bib.bib14); [Liu et al., 2026b](#bib.bib50)) (2 NFE) | 83.59 | 91.10 | 88.88 | 93.81 | 85.60 | 85.40 |
| TwinFlow ([Cheng et al., 2025](#bib.bib56); [Liu et al., 2026b](#bib.bib50)) (2 NFE) | 81.46 | 91.83 | 89.02 | 94.16 | 87.60 | 85.98 |
| Z-Image-Turbo++ ([Liu et al., 2026b](#bib.bib50)) (2 NFE) | 83.89 | 91.84 | 89.30 | 94.58 | 89.60 | 85.86 |
| TwinFlow (Qwen-Image) ([Cheng et al., 2025](#bib.bib56)) (1 NFE) | – | – | – | – | – | 86.52 |
| APEX (Qwen-Image) (LoRA&r=32) (1 NFE) | 93.12 | 90.95 | 91.38 | 90.65 | 91.73 | 86.17 |
| APEX (Qwen-Image) (LoRA&r=64) (1 NFE) | 92.46 | 91.14 | 90.71 | 91.30 | 91.98 | 85.77 |
| APEX (Qwen-Image) (Full) (1 NFE) | 93.25 | 89.76 | 90.65 | 91.17 | 90.75 | 84.59 |
| IDM (Z-Image) (LoRA&r=32) (2 NFE) | 80.04 | 92.78 | 89.47 | 94.43 | 89.46 | 86.03 |
| IDM (Z-Image) (LoRA&r=64) (2 NFE) | 80.46 | 92.94 | 89.59 | 94.52 | 89.74 | 86.44 |
| IDM (Z-Image) (Full) (2 NFE) | 80.85 | 93.08 | 89.70 | 94.60 | 90.00 | 86.82 |
| IDM (Z-Image) (LoRA&r=32) (1 NFE) | 79.56 | 92.60 | 89.34 | 94.32 | 89.14 | 85.56 |
| IDM (Z-Image) (LoRA&r=64) (1 NFE) | 79.96 | 92.75 | 89.45 | 94.41 | 89.40 | 85.95 |
| IDM (Z-Image) (Full) (1 NFE) | 80.33 | 92.89 | 89.55 | 94.49 | 89.65 | 86.31 |
| IDM (Qwen-Image) (LoRA&r=32) (2 NFE) | 93.29 | 90.06 | 91.02 | 91.38 | 92.02 | 86.44 |
| IDM (Qwen-Image) (LoRA&r=64) (2 NFE) | 93.68 | 90.20 | 91.13 | 91.46 | 92.28 | 86.82 |
| IDM (Qwen-Image) (Full) (2 NFE) | 94.03 | 90.33 | 91.23 | 91.53 | 92.52 | 87.16 |
| IDM (Qwen-Image) (LoRA&r=32) (1 NFE) | 92.74 | 89.86 | 90.86 | 91.26 | 91.66 | 85.91 |
| IDM (Qwen-Image) (LoRA&r=64) (1 NFE) | 93.12 | 90.00 | 90.97 | 91.34 | 91.92 | 86.28 |
| IDM (Qwen-Image) (Full) (1 NFE) | 93.46 | 90.12 | 91.07 | 91.41 | 92.14 | 86.61 |

### 5.3 Key Ablations

All controlled ablations use IDM (Z-Image) with full-parameter tuning at 2 NFE and the shared training configuration above. The default combines equal-weight DMD velocity and endpoint regression with ℒpop\mathcal{L}\_{\text{pop}} using generator EMA features.

Table 5: Overall ablation results across benchmarks (2 NFE). Scores are percentages. Row \raisebox{-0.05ex}{\tiny1}⃝ is the full configuration and the shared control; rows \raisebox{-0.05ex}{\tiny2}⃝–\raisebox{-0.05ex}{\tiny11}⃝ vary the losses, DMD regression weights, or feature map. The vv-only and xx-only controls retain ℒpop\mathcal{L}\_{\text{pop}}. APEX ([Liu et al., 2026a](#bib.bib61)) is the published Z-Image reference from its comparison with TwinFlow; rows \raisebox{-0.05ex}{\tiny12}⃝–\raisebox{-0.05ex}{\tiny16}⃝ are from [Liu et al. (2026b)](#bib.bib50), with row \raisebox{-0.05ex}{\tiny16}⃝ evaluated at 8 NFE.

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Idx | Model | NFE | OneIG | GenEval | DPG-Bench | LongText-CN | LongText-EN |
| Distribution Matching Loss Ablation | | | | | | | |
| \raisebox{-0.05ex}{\tiny2}⃝ | 00w/o ℒscore\mathcal{L}\_{\text{score}} (DMD loss) | 2 | 52.58 | 76.90 | 86.15 | 93.33 | 89.62 |
| \raisebox{-0.05ex}{\tiny3}⃝ | 00w/o ℒpop\mathcal{L}\_{\text{pop}} (feature-moment loss) | 2 | 52.87 | 77.46 | 86.54 | 93.87 | 89.79 |
| \raisebox{-0.05ex}{\tiny4}⃝ | 00w/o ℒscore\mathcal{L}\_{\text{score}} and ℒpop\mathcal{L}\_{\text{pop}} | 2 | 52.25 | 76.24 | 85.68 | 92.70 | 88.88 |
| DMD Regression Ablation | | | | | | | |
| \raisebox{-0.05ex}{\tiny5}⃝ | 00vv-loss only | 2 | 52.43 | 76.64 | 85.93 | 93.03 | 89.17 |
| \raisebox{-0.05ex}{\tiny6}⃝ | 00xx-loss only | 2 | 52.78 | 77.26 | 86.42 | 93.71 | 89.74 |
| \raisebox{-0.05ex}{\tiny7}⃝ | 002×\timesxx-loss+vv-loss | 2 | 53.01 | 77.71 | 86.75 | 94.17 | 90.13 |
| \raisebox{-0.05ex}{\tiny8}⃝ | 00xx-loss+2×\timesvv-loss | 2 | 52.95 | 77.59 | 86.66 | 94.05 | 90.04 |
| Feature-Map Ablation | | | | | | | |
| \raisebox{-0.05ex}{\tiny9}⃝ | 00DINOv2 | 2 | 53.00 | 77.75 | 86.71 | 94.13 | 90.09 |
| \raisebox{-0.05ex}{\tiny10}⃝ | 00Teacher features | 2 | 52.82 | 77.36 | 86.49 | 93.79 | 89.81 |
| \raisebox{-0.05ex}{\tiny11}⃝ | 00Live self-features | 2 | 52.91 | 77.51 | 86.60 | 93.95 | 89.95 |
| Comparative | | | | | | | |
| \raisebox{-0.05ex}{\tiny1}⃝ | IDM | 2 | 53.06 | 77.81 | 86.82 | 94.25 | 90.20 |
| \raisebox{-0.05ex}{\tiny15}⃝ | Z-Image-Turbo | 2 | 50.94 | 76.53 | 85.78 | 78.48 | 72.89 |
| \raisebox{-0.05ex}{\tiny13}⃝ | DMD2 | 2 | 50.70 | 76.12 | 85.40 | 85.30 | 80.99 |
| \raisebox{-0.05ex}{\tiny14}⃝ | TwinFlow | 2 | 51.38 | 72.41 | 85.98 | 78.65 | 71.99 |
| \raisebox{-0.05ex}{\tinyA}⃝ | APEX | 2 | 52.60 | 77.23 | 88.64 | 90.38 | 88.76 |
| \raisebox{-0.05ex}{\tiny12}⃝ | Z-Image-Turbo++ | 2 | 52.50 | 75.70 | 85.86 | 91.62 | 89.88 |
| Higher-NFE baseline | | | | | | | |
| \raisebox{-0.05ex}{\tiny16}⃝ | Z-Image-Turbo | 8 | 52.84 | 75.01 | 84.86 | 92.56 | 91.74 |

##### Added value of feature-moment matching.

Adding ℒpop\mathcal{L}\_{\text{pop}} to the shared DMD control raises GenEval from 77.46 to 77.81, LongText-CN from 93.87 to 94.25, and LongText-EN from 89.79 to 90.20, with gains on all five aggregate metrics. Removing ℒscore\mathcal{L}\_{\text{score}} instead gives 76.90 GenEval; removing both losses gives 76.24. The other two aggregate metrics also improve: OneIG rises from 52.87 to 53.06 and DPG-Bench from 86.54 to 86.82. The GenEval breakdown further identifies the gains from ℒpop\mathcal{L}\_{\text{pop}}: color-attribute binding rises from 65.25 to 66.25, position from 50.75 to 51.25, and counting from 70.94 to 71.25, with unchanged single- and two-object scores in [Table 6](#S5.T6 "Table 6 ‣ Qualitative comparison. ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching"). Removing DMD gives a larger GenEval decrease (0.91 points) than removing moment matching (0.35 points). Moment matching improves this DMD control while the score correction remains central.

##### Generator EMA features.

Moment matching with DINOv2 or generator EMA features improves all five metrics over the internal DMD control. From the same control without ℒpop\mathcal{L}\_{\text{pop}}, DINOv2 raises GenEval from 77.46 to 77.75 (+0.29 points), while EMA reaches 77.81 (+0.35). Their LongText-CN scores are close: 94.13 and 94.25. Live self-features and teacher features reach 77.51 and 77.36 GenEval. EMA features add moment supervision beyond internal DMD, with performance close to DINOv2 and no external feature encoder.

##### Velocity and endpoint regression.

To select how the DMD correction supervises predictions, we compare vv regression, xx regression, and their combinations while retaining ℒpop\mathcal{L}\_{\text{pop}}.

Both single-regression controls therefore include the added moment constraint, so this block tests how to apply DMD within the combined objective. Since ℓx​(t)=t2​ℓv​(t)\ell\_{x}(t)=t^{2}\ell\_{v}(t) in Eq. [12](#S4.E12 "In Velocity and endpoint regression. ‣ 4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching"), these choices change time weighting and update magnitude. Equal-weight v+xv{+}x reaches 77.81 GenEval, versus 76.64 for vv only and 77.26 for xx only; 2​x+v2x{+}v and x+2​vx{+}2v reach 77.71 and 77.59. Equal weights lead on the five aggregate metrics and are our empirical default, although x+2​vx{+}2v gives a higher position score, 52.00 versus 51.25. The mixed losses apply alternative weightings to the same detached correction; these results do not establish independent distributional information in the two regression terms.

##### Relation to APEX and the internal controls.

IDM builds on APEX’s internal velocity-difference construction ([Liu et al., 2026a](#bib.bib61)), adding endpoint regression and EMA feature-moment matching in [Figure 5](#S5.F5 "Figure 5 ‣ Relation to APEX and the internal controls. ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching"). The published APEX reference uses a smaller training collection, so the comparison reflects the complete training settings. IDM scores 90.20 on LongText-EN versus APEX’s 88.76, while APEX leads on DPG-Bench, 88.64 versus 86.82. Within the IDM training setting, the loss-removal and feature-map controls separate these objective choices from differences in training data.

![Refer to caption](2610.39633v1/Ablation-idm-losses.png)

Figure 5: Reference methods and IDM loss configurations. The two prompts are evaluated at 1 and 2 NFE. The v+xv{+}x control omits ℒpop\mathcal{L}\_{\text{pop}}, while full IDM includes EMA feature-moment matching. APEX is an external reference trained on a smaller collection; the IDM loss ablations share the same training setting.

##### Qualitative comparison.

In the examples of [Figure 5](#S5.F5 "Figure 5 ‣ Relation to APEX and the internal controls. ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching"), full IDM shows more consistent preservation of dense text across the displayed sampling budgets, particularly in the multi-line menu. The menu combines a prominent title with several rows of small characters, making it a demanding test of text rendering beyond a few large words. Its entries pair Chinese and English drink names, including Americano and Latte, with prices. Each row combines both scripts with numbers and currency symbols, all within the compact layout of a chalkboard menu. The v+xv{+}x control without ℒpop\mathcal{L}\_{\text{pop}} produces more saturated colors, most visibly in the orange and yellow regions of the sushi poster. The LongText results quantify text fidelity across the benchmark.

[Table 6](#S5.T6 "Table 6 ‣ Qualitative comparison. ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching"), [Table 7](#S5.T7 "Table 7 ‣ Qualitative comparison. ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching"), and [Table 8](#S5.T8 "Table 8 ‣ Qualitative comparison. ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching") expand the benchmark scores in [Table 5](#S5.T5 "Table 5 ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching") into their individual categories.

Table 6: Detailed GenEval ablation results. Scores are percentages; Overall is the mean of the six category scores. Configurations, row groups, and sources follow [Table 5](#S5.T5 "Table 5 ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching").

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Idx | Model | NFE | Overall | Two obj. | Color attr. | Position | Counting | Colors | Single obj. |
| Distribution Matching Loss Ablation | | | | | | | | | |
| \raisebox{-0.05ex}{\tiny2}⃝ | 00w/o ℒscore\mathcal{L}\_{\text{score}} (DMD loss) | 2 | 76.90 | 90.40 | 64.50 | 49.25 | 70.31 | 87.23 | 99.69 |
| \raisebox{-0.05ex}{\tiny3}⃝ | 00w/o ℒpop\mathcal{L}\_{\text{pop}} (feature-moment loss) | 2 | 77.46 | 90.91 | 65.25 | 50.75 | 70.94 | 87.23 | 99.69 |
| \raisebox{-0.05ex}{\tiny4}⃝ | 00w/o ℒscore\mathcal{L}\_{\text{score}} and ℒpop\mathcal{L}\_{\text{pop}} | 2 | 76.24 | 90.15 | 63.75 | 49.25 | 68.44 | 86.17 | 99.69 |
| DMD Regression Ablation | | | | | | | | | |
| \raisebox{-0.05ex}{\tiny5}⃝ | 00vv-loss only | 2 | 76.64 | 90.40 | 64.00 | 50.00 | 69.06 | 86.70 | 99.69 |
| \raisebox{-0.05ex}{\tiny6}⃝ | 00xx-loss only | 2 | 77.26 | 90.66 | 65.50 | 50.50 | 70.00 | 87.23 | 99.69 |
| \raisebox{-0.05ex}{\tiny7}⃝ | 002×\timesxx-loss+vv-loss | 2 | 77.71 | 91.16 | 65.75 | 51.25 | 70.63 | 87.77 | 99.69 |
| \raisebox{-0.05ex}{\tiny8}⃝ | 00xx-loss+2×\timesvv-loss | 2 | 77.59 | 91.16 | 66.00 | 52.00 | 70.00 | 86.70 | 99.69 |
| Feature-Map Ablation | | | | | | | | | |
| \raisebox{-0.05ex}{\tiny9}⃝ | 00DINOv2 | 2 | 77.75 | 91.16 | 65.75 | 51.75 | 70.94 | 87.23 | 99.69 |
| \raisebox{-0.05ex}{\tiny10}⃝ | 00Teacher features | 2 | 77.36 | 90.66 | 65.50 | 50.75 | 70.31 | 87.23 | 99.69 |
| \raisebox{-0.05ex}{\tiny11}⃝ | 00Live self-features | 2 | 77.51 | 90.91 | 66.00 | 51.25 | 70.00 | 87.23 | 99.69 |
| Comparative | | | | | | | | | |
| \raisebox{-0.05ex}{\tiny1}⃝ | IDM | 2 | 77.81 | 90.91 | 66.25 | 51.25 | 71.25 | 87.50 | 99.69 |
| \raisebox{-0.05ex}{\tiny15}⃝ | Z-Image-Turbo | 2 | 76.53 | 89.39 | 57.75 | 50.50 | 74.38 | 87.77 | 99.38 |
| \raisebox{-0.05ex}{\tiny13}⃝ | DMD2 | 2 | 76.12 | 90.40 | 65.50 | 49.00 | 67.50 | 84.31 | 100.00 |
| \raisebox{-0.05ex}{\tiny14}⃝ | TwinFlow | 2 | 72.41 | 87.12 | 54.75 | 40.00 | 67.81 | 85.11 | 99.69 |
| \raisebox{-0.05ex}{\tinyA}⃝ | APEX | 2 | 77.23 | 90.66 | 65.50 | 50.25 | 70.31 | 86.97 | 99.69 |
| \raisebox{-0.05ex}{\tiny12}⃝ | Z-Image-Turbo++ | 2 | 75.70 | 87.63 | 64.50 | 48.75 | 69.06 | 84.57 | 99.69 |
| Higher-NFE baseline | | | | | | | | | |
| \raisebox{-0.05ex}{\tiny16}⃝ | Z-Image-Turbo | 8 | 75.01 | 88.89 | 58.75 | 45.75 | 71.88 | 85.11 | 99.69 |

Table 7: Detailed DPG-Bench ablation results. Scores are percentages. Overall follows the standard prompt-level aggregation over the benchmark question hierarchy, rather than the mean of the five category columns. Configurations, row groups, and sources follow [Table 5](#S5.T5 "Table 5 ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching").

|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Idx | Model | NFE | Overall | Attribute | Global | Relation | Other | Entity |
| Distribution Matching Loss Ablation | | | | | | | | |
| \raisebox{-0.05ex}{\tiny2}⃝ | 00w/o ℒscore\mathcal{L}\_{\text{score}} (DMD loss) | 2 | 86.15 | 89.33 | 80.23 | 94.32 | 89.54 | 92.58 |
| \raisebox{-0.05ex}{\tiny3}⃝ | 00w/o ℒpop\mathcal{L}\_{\text{pop}} (feature-moment loss) | 2 | 86.54 | 89.54 | 79.94 | 94.48 | 89.41 | 92.88 |
| \raisebox{-0.05ex}{\tiny4}⃝ | 00w/o ℒscore\mathcal{L}\_{\text{score}} and ℒpop\mathcal{L}\_{\text{pop}} | 2 | 85.68 | 89.07 | 80.01 | 94.12 | 89.37 | 92.23 |
| DMD Regression Ablation | | | | | | | | |
| \raisebox{-0.05ex}{\tiny5}⃝ | 00vv-loss only | 2 | 85.93 | 89.21 | 79.45 | 94.22 | 89.05 | 92.42 |
| \raisebox{-0.05ex}{\tiny6}⃝ | 00xx-loss only | 2 | 86.42 | 89.48 | 79.56 | 94.43 | 89.15 | 92.78 |
| \raisebox{-0.05ex}{\tiny7}⃝ | 002×\timesxx-loss+vv-loss | 2 | 86.75 | 89.68 | 81.62 | 94.57 | 90.44 | 93.04 |
| \raisebox{-0.05ex}{\tiny8}⃝ | 00xx-loss+2×\timesvv-loss | 2 | 86.66 | 89.64 | 80.79 | 94.55 | 89.92 | 92.99 |
| Feature-Map Ablation | | | | | | | | |
| \raisebox{-0.05ex}{\tiny9}⃝ | 00DINOv2 | 2 | 86.71 | 89.66 | 82.26 | 94.56 | 90.85 | 92.87 |
| \raisebox{-0.05ex}{\tiny10}⃝ | 00Teacher features | 2 | 86.49 | 89.52 | 80.36 | 94.46 | 89.68 | 92.83 |
| \raisebox{-0.05ex}{\tiny11}⃝ | 00Live self-features | 2 | 86.60 | 89.58 | 80.97 | 94.51 | 90.08 | 92.91 |
| Comparative | | | | | | | | |
| \raisebox{-0.05ex}{\tiny1}⃝ | IDM | 2 | 86.82 | 89.70 | 80.85 | 94.60 | 90.00 | 93.08 |
| \raisebox{-0.05ex}{\tiny15}⃝ | Z-Image-Turbo | 2 | 85.78 | 88.78 | 84.19 | 94.16 | 89.60 | 91.73 |
| \raisebox{-0.05ex}{\tiny13}⃝ | DMD2 | 2 | 85.40 | 88.88 | 83.59 | 93.81 | 85.60 | 91.10 |
| \raisebox{-0.05ex}{\tiny14}⃝ | TwinFlow | 2 | 85.98 | 89.02 | 81.46 | 94.16 | 87.60 | 91.83 |
| \raisebox{-0.05ex}{\tinyA}⃝ | APEX | 2 | 88.64 | 90.20 | 88.35 | 95.10 | 90.80 | 92.88 |
| \raisebox{-0.05ex}{\tiny12}⃝ | Z-Image-Turbo++ | 2 | 85.86 | 89.30 | 83.89 | 94.58 | 89.60 | 91.84 |
| Higher-NFE baseline | | | | | | | | |
| \raisebox{-0.05ex}{\tiny16}⃝ | Z-Image-Turbo | 8 | 84.86 | 90.14 | 91.29 | 92.16 | 88.68 | 89.59 |

Table 8: Detailed OneIG ablation results. Scores are percentages; Overall is the mean of the five category scores. Configurations, row groups, and sources follow [Table 5](#S5.T5 "Table 5 ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching").

|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Idx | Model | NFE | Overall | Alignment | Text | Diversity | Style | Reasoning |
| Distribution Matching Loss Ablation | | | | | | | | |
| \raisebox{-0.05ex}{\tiny2}⃝ | 00w/o ℒscore\mathcal{L}\_{\text{score}} (DMD loss) | 2 | 52.58 | 86.13 | 97.09 | 12.74 | 38.04 | 28.90 |
| \raisebox{-0.05ex}{\tiny3}⃝ | 00w/o ℒpop\mathcal{L}\_{\text{pop}} (feature-moment loss) | 2 | 52.87 | 86.31 | 97.73 | 12.81 | 38.16 | 29.34 |
| \raisebox{-0.05ex}{\tiny4}⃝ | 00w/o ℒscore\mathcal{L}\_{\text{score}} and ℒpop\mathcal{L}\_{\text{pop}} | 2 | 52.25 | 85.94 | 96.37 | 12.67 | 37.90 | 28.37 |
| DMD Regression Ablation | | | | | | | | |
| \raisebox{-0.05ex}{\tiny5}⃝ | 00vv-loss only | 2 | 52.43 | 86.04 | 96.76 | 12.71 | 37.97 | 28.67 |
| \raisebox{-0.05ex}{\tiny6}⃝ | 00xx-loss only | 2 | 52.78 | 86.25 | 97.53 | 12.79 | 38.12 | 29.21 |
| \raisebox{-0.05ex}{\tiny7}⃝ | 002×\timesxx-loss+vv-loss | 2 | 53.01 | 86.39 | 98.06 | 12.84 | 38.22 | 29.54 |
| \raisebox{-0.05ex}{\tiny8}⃝ | 00xx-loss+2×\timesvv-loss | 2 | 52.95 | 86.36 | 97.94 | 12.83 | 38.20 | 29.42 |
| Feature-Map Ablation | | | | | | | | |
| \raisebox{-0.05ex}{\tiny9}⃝ | 00DINOv2 | 2 | 53.00 | 86.58 | 97.72 | 12.88 | 38.36 | 29.46 |
| \raisebox{-0.05ex}{\tiny10}⃝ | 00Teacher features | 2 | 52.82 | 86.28 | 97.62 | 12.80 | 38.14 | 29.26 |
| \raisebox{-0.05ex}{\tiny11}⃝ | 00Live self-features | 2 | 52.91 | 86.33 | 97.82 | 12.82 | 38.18 | 29.40 |
| Comparative | | | | | | | | |
| \raisebox{-0.05ex}{\tiny1}⃝ | IDM | 2 | 53.06 | 86.42 | 98.15 | 12.85 | 38.24 | 29.65 |
| \raisebox{-0.05ex}{\tiny15}⃝ | Z-Image-Turbo | 2 | 50.94 | 83.92 | 92.85 | 13.85 | 36.25 | 27.86 |
| \raisebox{-0.05ex}{\tiny13}⃝ | DMD2 | 2 | 50.70 | 85.21 | 90.82 | 12.75 | 36.77 | 27.93 |
| \raisebox{-0.05ex}{\tiny14}⃝ | TwinFlow | 2 | 51.38 | 85.26 | 90.61 | 15.49 | 38.03 | 27.52 |
| \raisebox{-0.05ex}{\tinyA}⃝ | APEX | 2 | 52.60 | 86.10 | 97.05 | 12.70 | 38.00 | 29.15 |
| \raisebox{-0.05ex}{\tiny12}⃝ | Z-Image-Turbo++ | 2 | 52.50 | 85.65 | 97.09 | 11.75 | 37.87 | 30.12 |
| Higher-NFE baseline | | | | | | | | |
| \raisebox{-0.05ex}{\tiny16}⃝ | Z-Image-Turbo | 8 | 52.84 | 84.03 | 99.32 | 13.85 | 36.81 | 30.19 |

![Refer to caption](2610.39633v1/NFE1.png)

Figure 6: Sampling-budget comparison on Z-Image. Final outputs from Z-Image-Turbo, DMD2, TwinFlow, APEX, and IDM at the indicated NFE budgets, grouped by two prompts. Each column represents a sampling budget, not an intermediate state of one trajectory.

### 5.4 Qualitative Results

[Figure 6](#S5.F6 "Figure 6 ‣ Qualitative comparison. ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching") compares sampling budgets. [Figure 2](#S1.F2 "Figure 2 ‣ 1 Introduction ‣ Intrinsic Distribution Matching") shows text rendering and portraits; [Figure 7](#S5.F7 "Figure 7 ‣ 5.4 Qualitative Results ‣ 5 Experiments ‣ Intrinsic Distribution Matching") provides additional samples across styles and content.

![Refer to caption](2610.39633v1/fig6.png)

![Refer to caption](2610.39633v1/fig9.png)

![Refer to caption](2610.39633v1/fig3.png)

![Refer to caption](2610.39633v1/fig4.png)

![Refer to caption](2610.39633v1/fig7.png)

![Refer to caption](2610.39633v1/fig8.png)

![Refer to caption](2610.39633v1/fig11.png)

![Refer to caption](2610.39633v1/fig12.png)

Figure 7: IDM (Z-Image), 2 NFE. Additional samples across styles and content. Every panel uses the same model and sampling budget; the grid is a gallery of outputs rather than a method or NFE comparison.

## 6 Conclusion

We presented Intrinsic Distribution Matching (IDM), which builds on internal DMD and adds an explicit constraint on generator EMA feature statistics. The reverse-KL field decomposition motivates retaining full score-difference supervision while additionally matching feature means and standard deviations. Controlled ablations show gains over the internal DMD baseline from EMA feature moments, with performance close to DINOv2. On Z-Image-Turbo 6B, IDM reaches 94.25% and 90.20% on Chinese and English LongText-Bench, the highest scores among the compared two-NFE methods. Experiments on backbones up to 20B parameters support using the generator’s predictions and representations together for few-step text-to-image generation.

## References

* Ambrosio and Savaré (2007)
  L. Ambrosio and G. Savaré
  Gradient flows of probability measures.
  In Handbook of differential equations: evolutionary equations,
  Vol. 3, pp. 1–136.
  Cited by: [§B.1.1](#A2.SS1.SSS1.p1.1 "B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Arjovsky et al. (2017)
  M. Arjovsky, S. Chintala, and L. Bottou
  Wasserstein generative adversarial networks.
  In International conference on machine learning,
  pp. 214–223.
  Cited by: [§B.1.1](#A2.SS1.SSS1.Px1.p1.1 "On condition (b): when does the model law admit a density? ‣ B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* BlackForest (2024)
  BlackForest
  FLUX.
  Note: <https://github.com/black-forest-labs/flux>
  Cited by: [Table 2](#S5.T2.4.1.7.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.7.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.12.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Cai et al. (2025)
  Q. Cai, J. Chen, Y. Chen, Y. Li, F. Long, Y. Pan, Z. Qiu, Y. Zhang, F. Gao, P. Xu, et al.
  HiDream-i1: a high-efficient image generative foundation model with sparse diffusion transformer.
  arXiv preprint arXiv:2505.22705.
  Cited by: [Table 2](#S5.T2.4.1.12.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.18.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chang et al. (2026)
  J. Chang, Y. Fang, P. Xing, S. Wu, W. Cheng, R. Wang, X. Zeng, G. Yu, and H. Chen
  Oneig-bench: omni-dimensional nuanced evaluation for image generation.
  Advances in Neural Information Processing Systems 38.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px5.p1.1 "Text Rendering in Image Generation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2026)
  C. Chen, H. Chen, K. Chen, Z. Cheng, L. Cui, R. Fang, Z. Gu, Z. Huang, Z. Lan, Y. Lei, et al.
  LLaDA-image: building strong image generators with fully open training recipes.
  arXiv preprint arXiv:2609.03796.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Chen et al. (2025a)
  J. Chen, Z. Xu, X. Pan, Y. Hu, C. Qin, T. Goldstein, L. Huang, T. Zhou, S. Xie, S. Savarese, et al.
  Blip3-o: a family of fully open unified multimodal models-architecture, training and dataset.
  arXiv preprint arXiv:2505.09568.
  Cited by: [§5.1](#S5.SS1.SSS0.Px2.p1.1 "Training data. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2024a)
  J. Chen, C. Ge, E. Xie, Y. Wu, L. Yao, X. Ren, Z. Wang, P. Luo, H. Lu, and Z. Li
  PixArt-Σ\Sigma: weak-to-strong training of diffusion transformer for 4k text-to-image generation.
  arXiv preprint arXiv:2403.04692.
  Cited by: [Table 4](#S5.T4.4.1.8.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2024b)
  J. Chen, C. Ge, E. Xie, Y. Wu, L. Yao, X. Ren, Z. Wang, P. Luo, H. Lu, and Z. Li
  Pixart-σ\sigma: weak-to-strong training of diffusion transformer for 4k text-to-image generation.
  arXiv preprint arXiv:2403.04692.
  Cited by: [Table 1](#S5.T1.8.1.24.1 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2024c)
  J. Chen, Y. Wu, S. Luo, E. Xie, S. Paul, P. Luo, H. Zhao, and Z. Li
  Pixart-{\{\\backslashdelta}\}: fast and controllable image generation with latent consistency models.
  arXiv preprint arXiv:2401.05252.
  Cited by: [Table 1](#S5.T1.8.1.23.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.4.1 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2025b)
  J. Chen, S. Xue, Y. Zhao, J. Yu, S. Paul, J. Chen, H. Cai, E. Xie, and S. Han
  SANA-sprint: one-step diffusion with continuous-time consistency distillation.
  arXiv preprint arXiv:2503.09641.
  Cited by: [Table 1](#S5.T1.8.1.10.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.29.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.30.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.9.1 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2024d)
  J. Chen, J. Yu, C. Ge, L. Yao, E. Xie, Z. Wang, J. T. Kwok, P. Luo, H. Lu, and Z. Li
  PixArt-α\alpha: fast training of diffusion transformer for photorealistic text-to-image synthesis.
  In ICLR,
  Cited by: [Table 2](#S5.T2.4.1.5.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.5.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.3.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2025c)
  J. Chen, Z. Cai, P. Chen, S. Chen, K. Ji, X. Wang, Y. Yang, and B. Wang
  ShareGPT-4o-image: aligning multimodal models with gpt-4o-level image generation.
  arXiv preprint arXiv:2506.18095.
  Cited by: [§5.1](#S5.SS1.SSS0.Px2.p1.1 "Training data. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2025d)
  X. Chen, Z. Wu, X. Liu, Z. Pan, W. Liu, Z. Xie, X. Yu, and C. Ruan
  Janus-pro: unified multimodal understanding and generation with data and model scaling.
  arXiv preprint arXiv:2501.17811.
  Cited by: [Table 2](#S5.T2.4.1.11.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.11.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.10.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.17.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Cheng et al. (2025)
  Z. Cheng, P. Sun, J. Li, and T. Lin
  TwinFlow: realizing one-step generation on large models with self-adversarial flows.
  arXiv preprint arXiv:2512.05150.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§B.4](#A2.SS4.p2.1 "B.4 DMD Loss: Score-Difference Identity and Regression ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p3.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px5.p1.1 "Internal Score Estimation. ‣ 2 Background ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.12.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.32.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.22.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.24.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.16.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.26.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.28.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Deng et al. (2025)
  C. Deng, D. Zhu, K. Li, C. Gou, F. Li, Z. Wang, S. Zhong, W. Yu, X. Nie, Z. Song, G. Shi, and H. Fan
  Emerging properties in unified multimodal pretraining.
  arXiv preprint arXiv:2505.14683.
  Cited by: [Table 2](#S5.T2.4.1.15.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.14.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Deng et al. (2026)
  M. Deng, H. Li, T. Li, Y. Du, and K. He
  Generative modeling via drifting.
  arXiv preprint arXiv:2602.04770.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Esser et al. (2024)
  P. Esser, S. Kulal, A. Blattmann, R. Entezari, J. Müller, H. Saini, Y. Levi, D. Lorenz, A. Sauer, F. Boesel, et al.
  Scaling rectified flow transformers for high-resolution image synthesis.
  In International Conference on Machine Learning,
  Cited by: [Table 1](#S5.T1.8.1.25.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.5.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.6.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.8.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.4.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.13.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.14.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.15.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Fang et al. (2025)
  R. Fang, A. Yu, C. Duan, L. Huang, S. Bai, Y. Cai, K. Wang, S. Liu, X. Liu, and H. Li
  Flux-reason-6m & prism-bench: a million-scale text-to-image reasoning dataset and comprehensive benchmark.
  arXiv preprint arXiv:2509.09680.
  Cited by: [§5.1](#S5.SS1.SSS0.Px2.p1.1 "Training data. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Franceschi et al. (2023)
  J. Franceschi, M. Gartrell, L. Dos Santos, T. Issenhuth, E. de Bézenac, M. Chen, and A. Rakotomamonjy
  Unifying gans and score-based diffusion as generative particle models.
  Advances in Neural Information Processing Systems 36, pp. 59729–59760.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Frans et al. (2024)
  K. Frans, D. Hafner, S. Levine, and P. Abbeel
  One step diffusion via shortcut models.
  arXiv preprint arXiv:2410.12557.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Gao et al. (2025)
  Y. Gao, L. Gong, Q. Guo, X. Hou, Z. Lai, F. Li, L. Li, X. Lian, C. Liao, L. Liu, et al.
  Seedream 3.0 technical report.
  arXiv preprint arXiv:2504.11346.
  Cited by: [Table 2](#S5.T2.4.1.14.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.20.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Geng et al. (2025a)
  Z. Geng, M. Deng, X. Bai, J. Z. Kolter, and K. He
  Mean flows for one-step generative modeling.
  arXiv preprint arXiv:2505.13447.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Geng et al. (2026)
  Z. Geng, Y. Lu, Z. Wu, E. Shechtman, J. Z. Kolter, and K. He
  Improved mean flows: on the challenges of fastforward generative models.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition,
  pp. 30467–30476.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Geng et al. (2025b)
  Z. Geng, Y. Wang, Y. Ma, C. Li, Y. Rao, S. Gu, Z. Zhong, Q. Lu, H. Hu, X. Zhang, et al.
  X-omni: reinforcement learning makes discrete autoregressive image generative models great again.
  arXiv preprint arXiv:2507.22058.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px5.p1.1 "Text Rendering in Image Generation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p6.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Ghosh et al. (2023)
  D. Ghosh, H. Hajishirzi, and L. Schmidt
  Geneval: an object-focused framework for evaluating text-to-image alignment.
  Advances in Neural Information Processing Systems 36, pp. 52132–52152.
  Cited by: [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Goodfellow et al. (2014)
  I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y. Bengio
  Generative adversarial nets.
  In Advances in Neural Information Processing Systems,
  Cited by: [§B.1.3](#A2.SS1.SSS3.Px2.p1.3 "Scaled Jensen–Shannon / saturating GAN. ‣ B.1.3 Important special cases ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Han et al. (2026a)
  J. Han, P. Li, Q. Guo, R. Xu, S. Ermon, and E. J. Candès
  One-step generative modeling via wasserstein gradient flows.
  arXiv preprint arXiv:2605.11755.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Han et al. (2026b)
  Y. Han, S. Liao, P. Sun, D. Liu, Y. Zhang, P. Wan, and T. Lin
  FlowCPO: a unified divergence view of preference alignment for flow models.
  arXiv preprint arXiv:2609.09905.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Heusel et al. (2017)
  M. Heusel, H. Ramsauer, T. Unterthiner, B. Nessler, and S. Hochreiter
  GANs trained by a two time-scale update rule converge to a local nash equilibrium.
  In Advances in Neural Information Processing Systems,
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Ho et al. (2020)
  J. Ho, A. Jain, and P. Abbeel
  Denoising diffusion probabilistic models.
  Advances in neural information processing systems 33, pp. 6840–6851.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Continuous Generative Models. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Holderrieth and Erives (2025)
  P. Holderrieth and E. Erives
  An introduction to flow matching and diffusion models.
  arXiv preprint arXiv:2506.02070.
  Cited by: [§B.3](#A2.SS3.p1.1 "B.3 Score–Velocity Identity ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Hu et al. (2024)
  X. Hu, R. Wang, Y. Fang, B. Fu, P. Cheng, and G. Yu
  Ella: equip diffusion models with llm for enhanced semantic alignment.
  arXiv preprint arXiv:2403.05135.
  Cited by: [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Labs (2024)
  B. F. Labs
  FLUX.
  External Links: [Link](https://blackforestlabs.ai/)
  Cited by: [Table 1](#S5.T1.8.1.28.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.8.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.16.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Li et al. (2017)
  C. Li, W. Chang, Y. Cheng, Y. Yang, and B. Póczos
  MMD GAN: towards deeper understanding of moment matching network.
  Advances in Neural Information Processing Systems 30.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Li et al. (2024a)
  D. Li, A. Kamko, E. Akhgari, A. Sabet, L. Xu, and S. Doshi
  Playground v2. 5: three insights towards enhancing aesthetic quality in text-to-image generation.
  arXiv preprint arXiv:2402.17245.
  Cited by: [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.6.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Li et al. (2015)
  Y. Li, K. Swersky, and R. Zemel
  Generative moment matching networks.
  In International Conference on Machine Learning,
  pp. 1718–1727.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Li et al. (2024b)
  Z. Li, J. Zhang, Q. Lin, J. Xiong, Y. Long, X. Deng, Y. Zhang, X. Liu, M. Huang, Z. Xiao, et al.
  Hunyuan-dit: a powerful multi-resolution diffusion transformer with fine-grained chinese understanding.
  arXiv preprint arXiv:2405.08748.
  Cited by: [Table 4](#S5.T4.4.1.6.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Lipman et al. (2022)
  Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le
  Flow matching for generative modeling.
  arXiv preprint arXiv:2210.02747.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Continuous Generative Models. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Liu et al. (2026a)
  D. Liu, P. Sun, Y. Han, Z. Cheng, C. Chen, and T. Lin
  Self-adversarial one step generation via condition shifting.
  arXiv preprint arXiv:2604.12322.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§B.4](#A2.SS4.p2.1 "B.4 DMD Loss: Score-Difference Identity and Regression ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p3.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px5.p1.1 "Internal Score Estimation. ‣ 2 Background ‣ Intrinsic Distribution Matching"),
  [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Internal velocity branches. ‣ 4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching"),
  [§5.1](#S5.SS1.SSS0.Px2.p1.1 "Training data. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [§5.3](#S5.SS3.SSS0.Px4.p1.1 "Relation to APEX and the internal controls. ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.13.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.14.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.15.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.33.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.34.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.35.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.18.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 5](#S5.T5 "In 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Liu et al. (2025)
  D. Liu, P. Sun, X. Li, and T. Lin
  Efficient generative model training via embedded representation warmup.
  arXiv preprint arXiv:2504.10188.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px4.p1.1 "Gaussian Score Structure and Intrinsic Representations. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Liu et al. (2026b)
  D. Liu, R. Du, D. Liu, D. Jiang, L. Li, Q. Wu, Z. Li, S. C. Hoi, H. Li, and P. Gao
  High-fidelity two-step image generation via teacher-aligned end-to-end distillation.
  arXiv preprint arXiv:2606.12575.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px5.p1.1 "Text Rendering in Image Generation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.20.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.21.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.22.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.23.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.24.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.25.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.26.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.27.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 5](#S5.T5 "In 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Liu et al. (2016)
  Q. Liu, J. Lee, and M. Jordan
  A kernelized stein discrepancy for goodness-of-fit tests.
  In International conference on machine learning,
  pp. 276–284.
  Cited by: [§B.2.2](#A2.SS2.SSS2.p1.1 "B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Liu et al. (2023)
  X. Liu, C. Gong, and Q. Liu
  Flow straight and fast: learning to generate and transfer data with rectified flow.
  In International Conference on Learning Representations,
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px2.p1.1 "Rectified Flow and Few-Step Generation. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Lu and Song (2024)
  C. Lu and Y. Song
  Simplifying, stabilizing and scaling continuous-time consistency models.
  arXiv preprint arXiv:2410.11081.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Lu et al. (2025)
  Y. Lu, X. Xia, M. Zhang, H. Kuang, J. Zheng, Y. Ren, and X. Xiao
  Hyper-bagel: a unified acceleration framework for multimodal understanding and generation.
  External Links: 2509.18824
  Cited by: [Table 2](#S5.T2.4.1.17.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Luo et al. (2023)
  S. Luo, Y. Tan, L. Huang, J. Li, and H. Zhao
  Latent consistency models: synthesizing high-resolution images with few-step inference.
  arXiv preprint arXiv:2310.04378.
  Cited by: [Table 1](#S5.T1.8.1.22.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.3.2 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Ma et al. (2025)
  Y. Ma, X. Liu, X. Chen, W. Liu, C. Wu, Z. Wu, Z. Pan, Z. Xie, H. Zhang, X. Yu, et al.
  Janusflow: harmonizing autoregression and rectified flow for unified multimodal understanding and generation.
  In Proceedings of the Computer Vision and Pattern Recognition Conference,
  pp. 7739–7751.
  Cited by: [Table 2](#S5.T2.4.1.9.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* ModelTC (2025)
  ModelTC
  Qwen-image-lightning.
   GitHub.
  Note: [GitHub-ModelTC/Qwen-Image-Lightning:Qwen-Image-Lightning:SpeedupQwen-Imagemodelwithdistilla](https://GitHub-ModelTC/Qwen-Image-Lightning:Qwen-Image-Lightning:SpeedupQwen-Imagemodelwithdistilla)
  Cited by: [Table 1](#S5.T1.8.1.11.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.31.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.18.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Niu et al. (2025)
  Y. Niu, M. Ning, M. Zheng, W. Jin, B. Lin, P. Jin, J. Liao, C. Feng, K. Ning, B. Zhu, et al.
  Wise: a world knowledge-informed semantic evaluation for text-to-image generation.
  arXiv preprint arXiv:2503.07265.
  Cited by: [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.2 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.3 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Nowozin et al. (2016)
  S. Nowozin, B. Cseke, and R. Tomioka
  F-gan: training generative neural samplers using variational divergence minimization.
  Advances in neural information processing systems 29.
  Cited by: [§B.1.2](#A2.SS1.SSS2.p2.1 "B.1.2 𝑓-divergence specialization ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* OpenAI (2023)
  OpenAI
  Dalle-3.
  External Links: [Link](https://openai.com/dall-e-3)
  Cited by: [Table 4](#S5.T4.4.1.11.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* OpenAI (2025)
  OpenAI
  GPT-image-1.
  External Links: [Link](https://openai.com/index/introducing-4o-image-generation/)
  Cited by: [Table 2](#S5.T2.4.1.13.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.15.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.21.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Pan et al. (2025)
  X. Pan, S. N. Shukla, A. Singh, Z. Zhao, S. K. Mishra, J. Wang, Z. Xu, J. Chen, K. Li, F. Juefei-Xu, et al.
  Transfer between modalities with metaqueries.
  arXiv preprint arXiv:2504.06256.
  Cited by: [Table 3](#S5.T3.4.1.13.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Podell et al. (2023)
  D. Podell, Z. English, K. Lacey, A. Blattmann, T. Dockhorn, J. Müller, J. Penna, and R. Rombach
  SDXL: improving latent diffusion models for high-resolution image synthesis.
  arXiv preprint arXiv:2307.01952.
  Cited by: [Table 3](#S5.T3.4.1.3.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.5.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Qin et al. (2025)
  Q. Qin, L. Zhuo, Y. Xin, R. Du, Z. Li, B. Fu, Y. Lu, J. Yuan, X. Li, D. Liu, et al.
  Lumina-image 2.0: a unified and efficient image generative framework.
  arXiv preprint arXiv:2503.21758.
  Cited by: [Table 2](#S5.T2.4.1.10.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.19.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Rombach et al. (2022)
  R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer
  High-resolution image synthesis with latent diffusion models.
  In IEEE Conference on Computer Vision and Pattern Recognition,
  Cited by: [Table 3](#S5.T3.4.1.2.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.2.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Salimans and Ho (2022)
  T. Salimans and J. Ho
  Progressive distillation for fast sampling of diffusion models.
  arXiv preprint arXiv:2202.00512.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Continuous Generative Models. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Sauer et al. (2024)
  A. Sauer, F. Boesel, T. Dockhorn, A. Blattmann, P. Esser, and R. Rombach
  Fast high-resolution image synthesis with latent adversarial diffusion distillation.
  arXiv preprint arXiv:2403.12015.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Sauer et al. (2023)
  A. Sauer, D. Lorenz, A. Blattmann, and R. Rombach
  Adversarial diffusion distillation.
  arXiv preprint arXiv:2311.17042.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Song et al. (2023)
  Y. Song, P. Dhariwal, M. Chen, and I. Sutskever
  Consistency models.
  In Proceedings of the 40th International Conference on Machine Learning,
  pp. 32211–32252.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Continuous Generative Models. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Song et al. (2020)
  Y. Song, J. Sohl-Dickstein, D. P. Kingma, A. Kumar, S. Ermon, and B. Poole
  Score-based generative modeling through stochastic differential equations.
  arXiv preprint arXiv:2011.13456.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Continuous Generative Models. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Sun et al. (2026a)
  P. Sun, Z. Cheng, D. Liu, J. Xie, X. Shang, and T. Lin
  Three-body scattering for generative modeling.
  arXiv preprint arXiv:2607.18198.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Sun and Lin (2025)
  P. Sun and T. Lin
  Any-step generation via n-th order recursive consistent velocity field estimation.
  Note: GitHub repository
  External Links: [Link](https://github.com/LINs-lab/RCGM)
  Cited by: [§4.3](#S4.SS3.p1.1 "4.3 Training Objective ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching").
* Sun et al. (2026b)
  P. Sun, X. Shang, T. Lin, and Z. Shen
  Duality models: an embarrassingly simple one-step generation paradigm.
  arXiv preprint arXiv:2602.17682.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Team (2025)
  Z. Team
  Z-image: an efficient image generation foundation model with single-stream diffusion transformer.
  arXiv preprint arXiv:2511.22699.
  Cited by: [§5.1](#S5.SS1.SSS0.Px1.p1.1 "Backbones and tuning. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.19.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.20.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.23.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.24.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Wang and Vastola (2023)
  B. Wang and J. J. Vastola
  The hidden linear structure in score-based models and its application.
  arXiv preprint arXiv:2311.10892.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px4.p1.1 "Gaussian Score Structure and Intrinsic Representations. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p4.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§3.3](#S3.SS3.p1.2 "3.3 Decomposition of the Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching").
* Wang and Vastola (2024)
  B. Wang and J. J. Vastola
  The unreasonable effectiveness of gaussian score approximation for diffusion models and its applications.
  arXiv preprint arXiv:2412.09726.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px4.p1.1 "Gaussian Score Structure and Intrinsic Representations. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p4.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§3.3](#S3.SS3.p1.2 "3.3 Decomposition of the Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching").
* Wang et al. (2024a)
  F. Wang, Z. Huang, A. W. Bergman, D. Shen, P. Gao, M. Lingelbach, K. Sun, W. Bian, G. Song, Y. Liu, et al.
  Phased consistency model.
  arXiv preprint arXiv:2405.18407.
  Cited by: [Table 1](#S5.T1.8.1.26.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.6.1 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Wang et al. (2024b)
  X. Wang, X. Zhang, Z. Luo, Q. Sun, Y. Cui, J. Wang, F. Zhang, Y. Wang, Z. Li, Q. Yu, et al.
  Emu3: next-token prediction is all you need.
  arXiv preprint arXiv:2409.18869.
  Cited by: [Table 2](#S5.T2.4.1.4.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.12.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.9.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Wang et al. (2026)
  Y. Wang, W. Bai, D. Zhang, W. Luo, H. Sun, et al.
  Uni-instruct: one-step diffusion model through unified diffusion divergence instruction.
  Advances in Neural Information Processing Systems 38, pp. 57097–57132.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§B.1.3](#A2.SS1.SSS3.p1.1 "B.1.3 Important special cases ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Wang et al. (2023)
  Z. Wang, C. Lu, Y. Wang, F. Bao, C. Li, H. Su, and J. Zhu
  ProlificDreamer: high-fidelity and diverse text-to-3d generation with variational score distillation.
  Advances in Neural Information Processing Systems 36, pp. 8406–8441.
  Cited by: [§2](#S2.SS0.SSS0.Px3.p1.1 "Distribution Matching Distillation. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Weber (2023)
  R. M. Weber
  The score-difference flow for implicit generative modeling.
  arXiv preprint arXiv:2304.12906.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Wu et al. (2025a)
  C. Wu, J. Li, J. Zhou, J. Lin, K. Gao, K. Yan, S. Yin, S. Bai, X. Xu, Y. Chen, et al.
  Qwen-image technical report.
  arXiv preprint arXiv:2508.02324.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px5.p1.1 "Text Rendering in Image Generation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§5.1](#S5.SS1.SSS0.Px1.p1.1 "Backbones and tuning. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.16.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.22.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Wu et al. (2025b)
  C. Wu, X. Chen, Z. Wu, Y. Ma, X. Liu, Z. Pan, W. Liu, Z. Xie, X. Yu, C. Ruan, et al.
  Janus: decoupling visual encoding for unified multimodal understanding and generation.
  In Proceedings of the Computer Vision and Pattern Recognition Conference,
  pp. 12966–12977.
  Cited by: [Table 3](#S5.T3.4.1.8.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.7.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Wu et al. (2024)
  Y. Wu, Z. Zhang, J. Chen, H. Tang, D. Li, Y. Fang, L. Zhu, E. Xie, H. Yin, L. Yi, et al.
  Vila-u: a unified foundation model integrating visual understanding and generation.
  arXiv preprint arXiv:2409.04429.
  Cited by: [Table 3](#S5.T3.4.1.9.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Xie et al. (2024)
  J. Xie, W. Mao, Z. Bai, D. J. Zhang, W. Wang, K. Q. Lin, Y. Gu, Z. Chen, Z. Yang, and M. Z. Shou
  Show-o: one single transformer to unify multimodal understanding and generation.
  arXiv preprint arXiv:2408.12528.
  Cited by: [Table 2](#S5.T2.4.1.3.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.10.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Xu et al. (2025)
  Y. Xu, W. Nie, and A. Vahdat
  One-step diffusion models with ff-divergence distribution matching.
  arXiv preprint arXiv:2502.15681.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§B.1.2](#A2.SS1.SSS2.p2.1 "B.1.2 𝑓-divergence specialization ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"),
  [§B.1.3](#A2.SS1.SSS3.p1.1 "B.1.3 Important special cases ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Yang et al. (2026)
  J. Yang, Z. Geng, X. Ju, Y. Tian, and Y. Wang
  Representation fréchet loss for visual generation.
  arXiv:2604.28190.
  External Links: [Link](https://arxiv.org/abs/2604.28190)
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p5.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§4.2](#S4.SS2.SSS0.Px1.p1.1 "Intrinsic feature map. ‣ 4.2 Feature-Moment Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching").
* Yi et al. (2023)
  M. Yi, Z. Zhu, and S. Liu
  Monoflow: rethinking divergence gans via the perspective of wasserstein gradient flows.
  In International Conference on Machine Learning,
  pp. 39984–40000.
  Cited by: [§B.1.3](#A2.SS1.SSS3.p1.1 "B.1.3 Important special cases ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Yin et al. (2024a)
  T. Yin, M. Gharbi, T. Park, R. Zhang, E. Shechtman, F. Durand, and W. T. Freeman
  Improved distribution matching distillation for fast image synthesis.
  arXiv:2405.14867.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p2.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.27.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.7.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.21.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.25.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Yin et al. (2024b)
  T. Yin, M. Gharbi, R. Zhang, E. Shechtman, F. Durand, W. T. Freeman, and T. Park
  One-step diffusion with distribution matching distillation.
  In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition,
  pp. 6613–6623.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§B.1.3](#A2.SS1.SSS3.Px1.p1.2 "Reverse KL / DMD. ‣ B.1.3 Important special cases ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p2.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px3.p1.1 "Distribution Matching Distillation. ‣ 2 Background ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.24.1 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Yu et al. (2024)
  S. Yu, S. Kwak, H. Jang, J. Jeong, J. Huang, J. Shin, and S. Xie
  Representation alignment for generation: training diffusion transformers is easier than you think.
  arXiv preprint arXiv:2410.06940.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px4.p1.1 "Gaussian Score Structure and Intrinsic Representations. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Zhang et al. (2026a)
  J. Zhang, K. Jiang, J. Chen, X. Wang, D. Liu, J. Li, D. Chen, M. Lin, J. Zhou, H. Jin, et al.
  Vidu s2: real-time interactive, editable, and spatial video generation.
  arXiv preprint arXiv:2609.11638.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Zhang et al. (2026b)
  Y. Zhang, C. Li, G. Ma, J. Zha, Y. Yang, B. Wang, W. Tang, W. Li, H. Huang, and N. Duan
  Teacher-feature drifting: one-step diffusion distillation with pretrained diffusion representations.
  arXiv preprint arXiv:2605.07327.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p5.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§4.2](#S4.SS2.SSS0.Px1.p1.1 "Intrinsic feature map. ‣ 4.2 Feature-Moment Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching").
* Zheng et al. (2025)
  K. Zheng, Y. Wang, Q. Ma, H. Chen, J. Zhang, Y. Balaji, J. Chen, M. Liu, J. Zhu, and Q. Zhang
  Large scale diffusion distillation via score-regularized continuous-time consistency.
  arXiv preprint arXiv:2510.08431.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p2.1 "1 Introduction ‣ Intrinsic Distribution Matching").
* Zhuo et al. (2024)
  L. Zhuo, R. Du, H. Xiao, Y. Li, D. Liu, R. Huang, W. Liu, X. Zhu, F. Wang, Z. Ma, et al.
  Lumina-next: making lumina-t2x stronger and faster with next-dit.
  Advances in Neural Information Processing Systems 37, pp. 131278–131315.
  Cited by: [Table 4](#S5.T4.4.1.4.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").

## Appendix A Related Work

##### Fast Generative Models.

Progressive distillation, consistency models, shortcut models, and MeanFlow reduce sampling steps by learning transitions or relations along a generative trajectory ([Salimans and Ho, 2022](#bib.bib54); [Song et al., 2023](#bib.bib52); [Lu and Song, 2024](#bib.bib53); [Frans et al., 2024](#bib.bib51); [Geng et al., 2025a](#bib.bib55); [Geng et al., 2026](#bib.bib62)). Duality Models jointly predict velocities and flow maps with a shared backbone ([Sun et al., 2026b](#bib.bib84)). Distributional approaches use adversarial or score-based supervision to train generated outputs directly ([Sauer et al., 2023](#bib.bib7); [Sauer et al., 2024](#bib.bib6); [Yin et al., 2024b](#bib.bib16); [Yin et al., 2024a](#bib.bib14)). rCM combines continuous-time consistency with score regularization and demonstrates their complementarity on large image and video models ([Zheng et al., 2025](#bib.bib66)). LLaDA-Image-Turbo supports inference in two to four steps, while Vidu S2 targets real-time interactive video generation and editing ([Chen et al., 2026](#bib.bib87); [Zhang et al., 2026a](#bib.bib85)). IDM studies distributional supervision from the generator itself.

##### Distribution Gradients and Internal Score Estimation.

DMD estimates the score difference between noised reference and generated distributions using a reference network and an online fake-score model ([Yin et al., 2024b](#bib.bib16)); DMD2 adds adversarial supervision and techniques for stable few-step distillation ([Yin et al., 2024a](#bib.bib14)). Related work connects adversarial and score-based updates through sample-space fields ([Franceschi et al., 2023](#bib.bib76); [Weber, 2023](#bib.bib77)) and extends distribution matching to broader divergence families ([Xu et al., 2025](#bib.bib68); [Wang et al., 2026](#bib.bib69)). FlowCPO develops an offline forward-KL formulation for preference alignment in flow models ([Han et al., 2026b](#bib.bib86)). TwinFlow and APEX estimate score differences through internally separated velocity branches ([Cheng et al., 2025](#bib.bib56); [Liu et al., 2026a](#bib.bib61)). IDM adds a feature-moment loss to internal DMD.

##### Feature-Space Distribution Matching.

GMMN and MMD-GAN use moment or kernel discrepancies for generative training ([Li et al., 2015](#bib.bib72); [Li et al., 2017](#bib.bib73)). FD-Loss turns a full-covariance Gaussian feature discrepancy into a training objective and uses queue or EMA estimators to connect population statistics with batch gradients ([Heusel et al., 2017](#bib.bib5); [Yang et al., 2026](#bib.bib65)). Three-Body Scattering derives one-step regression targets from energy-distance interactions in frozen features ([Sun et al., 2026a](#bib.bib81)). Drifting and W-Flow construct distributional updates through kernel interactions and batchwise optimal transport, respectively ([Deng et al., 2026](#bib.bib64); [Han et al., 2026a](#bib.bib63)), while Teacher-Feature Drifting uses representations from a pretrained teacher ([Zhang et al., 2026b](#bib.bib67)). IDM instead matches feature means and per-coordinate standard deviations in the generator’s EMA feature space.

##### Gaussian Score Structure and Intrinsic Representations.

The Gaussian-plus-residual score representation of [Wang and Vastola (2023)](#bib.bib79); [Wang and Vastola (2024)](#bib.bib80) underlies our reverse-KL field decomposition and motivates an additional feature-moment constraint. REPA shows that diffusion-transformer hidden states contain useful semantic information and can be strengthened through external representation alignment ([Yu et al., 2024](#bib.bib11)). Embedded Representation Warmup adds a dedicated representation-alignment stage before generative training ([Liu et al., 2025](#bib.bib60)). Our EMA feature map reuses such internal representations and evolves with the generator; its utility is evaluated against external, teacher, and live self-feature alternatives in [Section 5.3](#S5.SS3 "5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching").

##### Text Rendering in Image Generation.

Recent text-to-image models, including Qwen-Image and X-Omni, place increasing emphasis on accurate text rendering ([Wu et al., 2025a](#bib.bib33); [Geng et al., 2025b](#bib.bib83)). LongText-Bench evaluates extended Chinese and English text across multiple scenarios ([Geng et al., 2025b](#bib.bib83)), complementing the broader dimensions assessed by OneIG ([Chang et al., 2026](#bib.bib82)). Z-Image-Turbo++ reports LongText as a sensitive measure of text quality under a limited sampling budget ([Liu et al., 2026b](#bib.bib50)). We focus on LongText performance at 2 NFE.

## Appendix B Theoretical Proofs

##### Conventions.

The distribution-gradient and score identities are stated at fixed condition 𝐜∼pc\mathbf{c}\sim p\_{c}, with conditioning omitted when unambiguous; training averages the resulting conditional gradients over 𝐜\mathbf{c}. In contrast, feature moments pool samples from the joint law pi​(𝐱∣𝐜)​pc​(𝐜)p\_{i}(\mathbf{x}\mid\mathbf{c})p\_{c}(\mathbf{c}). A subscript tt denotes a noisy marginal, a star an exact marginal quantity, and a hat a learned or empirical estimate. Thus ℒpop\mathcal{L}\_{\text{pop}} denotes the population moment loss and ℒ^pop\widehat{\mathcal{L}}\_{\text{pop}} its empirical counterpart. For full queues of equal size KK, the model estimator uses Nϕ=B+KN\_{\phi}=B+K features, where BB is the global current-batch size; the reference estimator uses the KK queued reference features.

### B.1 Unified Gradient Structure

#### B.1.1 First variation form

We give regularity assumptions and prove the general identity behind ([5](#S3.E5 "In 3.2 Parameter Gradient ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching")).
We use the standard first-variation calculation for functionals of a density obeying a continuity equation, in the sense of gradient flows of probability measures ([Ambrosio and Savaré, 2007](#bib.bib78)). The pushforward step converts the sample-space integral into an expectation over the noise prior and clarifies its dependence on generator parameters.

###### Definition B.1 (Distribution Gradient) .

For a distributional discrepancy 𝒟⁡(pθ,pr)\mathcal{D}(p\_{\theta},p\_{r}) admitting a differentiable first-variation potential ψ⁡(𝐱):=δ​𝒟​(pθ,pr)/δ​pθ​(𝐱)\psi(\mathbf{x}):=\delta\mathcal{D}(p\_{\theta},p\_{r})/\delta p\_{\theta}(\mathbf{x}), the *sample-space distribution gradient* is

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐠𝒟​(𝐱):=∇𝐱ψ​(𝐱).\mathbf{g}\_{\mathcal{D}}(\mathbf{x}):=\nabla\_{\mathbf{x}}\psi(\mathbf{x}). |  | (15) |

###### Assumption 1 (Regularity for the first variation) .

Fix 𝐜\mathbf{c} and let Gθ​(⋅,𝐜)G\_{\theta}(\cdot,\mathbf{c}) push pzp\_{z} to pθ(⋅∣𝐜)p\_{\theta}(\cdot\mid\mathbf{c}). The reference law prp\_{r} is fixed, and the discrepancy depends on θ\theta only through pθp\_{\theta}.
For each direction Δ​θ\Delta\theta, define
θϵ=θ+ϵ​Δ​θ\theta\_{\epsilon}=\theta+\epsilon\Delta\theta and
pθϵ:=(Gθϵ​(⋅,𝐜))#​pzp\_{\theta\_{\epsilon}}:=(G\_{\theta\_{\epsilon}}(\cdot,\mathbf{c}))\_{\#}p\_{z}.

(a)

GθG\_{\theta} is differentiable in θ\theta,
(b)

pθϵp\_{\theta\_{\epsilon}} admits a smooth density near ϵ=0\epsilon=0, and differentiation can be exchanged with the relevant integrals.
(c)

For any first-variation potential ψ\psi used below, the boundary term in integration by parts vanishes; for example, ψ⁡(𝐱)​pθ​(𝐱)​𝐮​(𝐱)\psi(\mathbf{x})p\_{\theta}(\mathbf{x})\mathbf{u}(\mathbf{x}) decays sufficiently fast as ‖𝐱‖→∞\|\mathbf{x}\|\to\infty.

##### On condition (b): when does the model law admit a density?

Condition (b) is an assumption rather than a consequence of the generator construction.
For a locally Lipschitz deterministic map Gθ​(⋅,𝐜):ℝd→ℝdG\_{\theta}(\cdot,\mathbf{c}):\mathbb{R}^{d}\to\mathbb{R}^{d}, the area formula implies that a Jacobian ∂Gθ/∂𝐳\partial G\_{\theta}/\partial\mathbf{z} singular on a set of positive pzp\_{z}-measure produces a singular component in the image law. The full model law then has no Lebesgue density, so its clean score 𝐬θ=∇𝐱​log​pθ\mathbf{s}\_{\theta}=\nabla\_{\mathbf{x}}\log p\_{\theta} is not defined as assumed.
This is not a pathological case. A generator that collapses a direction of the seed space, for instance one that has learned to ignore part of 𝐳\mathbf{z}, produces exactly this degeneracy.
It is the same manifold-support obstruction identified by [Arjovsky et al. (2017)](#bib.bib57) for implicit generators, which there motivates replacing ff-divergences by a weaker metric; we instead retain the divergence and carry the density assumption explicitly.

The clean-distribution results in [Section 3](#S3 "3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching") therefore assume smooth, strictly positive densities on a common domain, together with the integrability and boundary conditions required by each result. The factorization ([5](#S3.E5 "In 3.2 Parameter Gradient ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching")), reverse-KL field ([3](#S3.E3 "In 3.1 Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching")), and decomposition ([7](#S3.E7 "In 3.3 Decomposition of the Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching")) are exact within that setting.
This restriction is distinct from the noisy-marginal setting: adding independent nondegenerate Gaussian noise gives a smooth positive density for every t∈(0,1)t\in(0,1), even when the clean law is singular. The score–velocity identity in [Appendix B.3](#A2.SS3 "B.3 Score–Velocity Identity ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching") therefore does not require a clean density; its finite-second-moment assumption suffices for the stated velocity regression. A noisy reverse-KL objective additionally requires the relevant divergence and gradient integrals to exist.
The practical losses in [Section 4](#S4 "4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching") remain computable without evaluating clean scores. Singular clean laws invalidate the clean-field interpretation, but do not by themselves invalidate the noisy score fields or feature-moment objective.

###### Proof B.2 (Proof of ([5](#S3.E5 "In 3.2 Parameter Gradient ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching"))) .

Fix an arbitrary direction Δ​θ\Delta\theta and write θϵ=θ+ϵ​Δ​θ\theta\_{\epsilon}=\theta+\epsilon\Delta\theta. For 𝐱=Gθ​(𝐳,𝐜)\mathbf{x}=G\_{\theta}(\mathbf{z},\mathbf{c}), the generated sample has the first-order expansion:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐱θϵ=Gθ+ϵ​Δ​θ​(𝐳,𝐜)=𝐱+ϵ​𝐮𝐳+o⁡(ϵ),𝐮𝐳:=Jθ​Gθ​(𝐳,𝐜)​Δ​θ.\mathbf{x}\_{\theta\_{\epsilon}}=G\_{\theta+\epsilon\Delta\theta}(\mathbf{z},\mathbf{c})=\mathbf{x}+\epsilon\mathbf{u}\_{\mathbf{z}}+o(\epsilon),\qquad\mathbf{u}\_{\mathbf{z}}:=J\_{\theta}G\_{\theta}(\mathbf{z},\mathbf{c})\Delta\theta. |  | (16) |

The corresponding velocity field is the conditional mean displacement of samples currently located at 𝐱\mathbf{x}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐮⁡(𝐱):=𝔼⁡[𝐮𝐳∣Gθ​(𝐳,𝐜)=𝐱].\mathbf{u}(\mathbf{x}):=\mathbb{E}\!\left[\mathbf{u}\_{\mathbf{z}}\mid G\_{\theta}(\mathbf{z},\mathbf{c})=\mathbf{x}\right]. |  | (17) |

We first identify the density perturbation induced by this sample displacement. For any smooth compactly supported test function φ\varphi, the pushforward definition and ([16](#A2.E16 "In Proof B.2 (Proof of ()) . ‣ On condition (b): when does the model law admit a density? ‣ B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) give

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | dd​ϵ​∫φ⁡(𝐱)​pθϵ​(𝐱)​𝑑𝐱|ϵ=0\displaystyle\frac{d}{d\epsilon}\int\varphi(\mathbf{x})p\_{\theta\_{\epsilon}}(\mathbf{x})\,\mathrm{d}\mathbf{x}\bigg|\_{\epsilon=0} | =dd​ϵ​𝔼𝐳​[φ⁡(Gθ+ϵ​Δ​θ​(𝐳,𝐜))]|ϵ=0\displaystyle=\frac{d}{d\epsilon}\mathbb{E}\_{\mathbf{z}}\left[\varphi(G\_{\theta+\epsilon\Delta\theta}(\mathbf{z},\mathbf{c}))\right]\bigg|\_{\epsilon=0} |  | (18) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =dd​ϵ​𝔼𝐳​[φ⁡(𝐱+ϵ​𝐮𝐳)]|ϵ=0\displaystyle=\frac{d}{d\epsilon}\mathbb{E}\_{\mathbf{z}}\left[\varphi(\mathbf{x}+\epsilon\mathbf{u}\_{\mathbf{z}})\right]\bigg|\_{\epsilon=0} |  | (19) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =𝔼𝐳​[∇𝐱φ​(Gθ​(𝐳,𝐜))⊤​𝐮𝐳]\displaystyle=\mathbb{E}\_{\mathbf{z}}\left[\nabla\_{\mathbf{x}}\varphi(G\_{\theta}(\mathbf{z},\mathbf{c}))^{\top}\mathbf{u}\_{\mathbf{z}}\right] |  | (20) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =∫∇𝐱φ​(𝐱)⊤​pθ​(𝐱)​𝐮​(𝐱)​𝑑𝐱.\displaystyle=\int\nabla\_{\mathbf{x}}\varphi(\mathbf{x})^{\top}p\_{\theta}(\mathbf{x})\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x}. |  | (21) |

The last equality is exactly the conditional-expectation definition of 𝐮⁡(𝐱)\mathbf{u}(\mathbf{x}). Since ([21](#A2.E21 "In Proof B.2 (Proof of ()) . ‣ On condition (b): when does the model law admit a density? ‣ B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) holds for all such φ\varphi, the density path satisfies the continuity equation in the weak sense:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∂ϵpθϵ(𝐱)|ϵ=0=−∇𝐱⋅(pθ(𝐱)𝐮(𝐱)).\partial\_{\epsilon}p\_{\theta\_{\epsilon}}(\mathbf{x})\big|\_{\epsilon=0}=-\nabla\_{\mathbf{x}}\cdot(p\_{\theta}(\mathbf{x})\mathbf{u}(\mathbf{x})). |  | (22) |

Now consider a distributional discrepancy 𝒟⁡(pθ,pr)\mathcal{D}(p\_{\theta},p\_{r}) with first variation

|  |  |  |  |
| --- | --- | --- | --- |
|  | ψ​(𝐱):=δ​𝒟​(pθ,pr)δ​pθ​(𝐱),\psi(\mathbf{x}):=\frac{\delta\mathcal{D}(p\_{\theta},p\_{r})}{\delta p\_{\theta}}(\mathbf{x}), |  | (23) |

meaning that, along the density path pθϵp\_{\theta\_{\epsilon}},

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | dd​ϵ​𝒟​(pθϵ,pr)|ϵ=0\displaystyle\frac{d}{d\epsilon}\mathcal{D}(p\_{\theta\_{\epsilon}},p\_{r})\bigg|\_{\epsilon=0} | =∫ψ⁡(𝐱)​∂ϵpθϵ​(𝐱)|ϵ=0​𝑑𝐱\displaystyle=\int\psi(\mathbf{x})\,\partial\_{\epsilon}p\_{\theta\_{\epsilon}}(\mathbf{x})\big|\_{\epsilon=0}\,\mathrm{d}\mathbf{x} |  | (24) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =−∫ψ(𝐱)∇𝐱⋅(pθ(𝐱)𝐮(𝐱))d𝐱\displaystyle=-\int\psi(\mathbf{x})\,\nabla\_{\mathbf{x}}\cdot(p\_{\theta}(\mathbf{x})\mathbf{u}(\mathbf{x}))\,\mathrm{d}\mathbf{x} |  | (25) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =∫∇𝐱ψ​(𝐱)⋅pθ​(𝐱)​𝐮​(𝐱)​𝑑𝐱,\displaystyle=\int\nabla\_{\mathbf{x}}\psi(\mathbf{x})\cdot p\_{\theta}(\mathbf{x})\,\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x}, |  | (26) |

where the last equality is integration by parts, using the vanishing boundary term in [Assump. 1](#Thminnerassumption1 "Assumption 1 (Regularity for the first variation) . ‣ B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")(c). By ([17](#A2.E17 "In Proof B.2 (Proof of ()) . ‣ On condition (b): when does the model law admit a density? ‣ B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")), any integrable vector field
𝐰⁡(𝐱)\mathbf{w}(\mathbf{x}) satisfies the following pushforward-expectation identity (converting an expectation under pθp\_{\theta} to one under the noise prior):

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∫pθ​(𝐱)​𝐰​(𝐱)⊤​𝐮​(𝐱)​𝑑𝐱=𝔼𝐳​[𝐰​(Gθ​(𝐳,𝐜))⊤​𝐮𝐳].\int p\_{\theta}(\mathbf{x})\,\mathbf{w}(\mathbf{x})^{\top}\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x}=\mathbb{E}\_{\mathbf{z}}\left[\mathbf{w}(G\_{\theta}(\mathbf{z},\mathbf{c}))^{\top}\mathbf{u}\_{\mathbf{z}}\right]. |  | (27) |

Taking 𝐰=∇𝐱ψ\mathbf{w}=\nabla\_{\mathbf{x}}\psi in ([27](#A2.E27 "In Proof B.2 (Proof of ()) . ‣ On condition (b): when does the model law admit a density? ‣ B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) gives

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∫pθ​(𝐱)​∇𝐱ψ​(𝐱)⋅𝐮⁡(𝐱)​𝑑𝐱=𝔼𝐳​[∇𝐱ψ​(Gθ​(𝐳,𝐜))⊤​𝐮𝐳]=𝔼𝐳​[∇𝐱ψ​(Gθ​(𝐳,𝐜))⊤​Jθ​Gθ​(𝐳,𝐜)​Δ​θ].\int p\_{\theta}(\mathbf{x})\,\nabla\_{\mathbf{x}}\psi(\mathbf{x})\cdot\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x}=\mathbb{E}\_{\mathbf{z}}\left[\nabla\_{\mathbf{x}}\psi(G\_{\theta}(\mathbf{z},\mathbf{c}))^{\top}\mathbf{u}\_{\mathbf{z}}\right]=\mathbb{E}\_{\mathbf{z}}\left[\nabla\_{\mathbf{x}}\psi(G\_{\theta}(\mathbf{z},\mathbf{c}))^{\top}J\_{\theta}G\_{\theta}(\mathbf{z},\mathbf{c})\Delta\theta\right]. |  | (28) |

Combining ([26](#A2.E26 "In Proof B.2 (Proof of ()) . ‣ On condition (b): when does the model law admit a density? ‣ B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) and
([28](#A2.E28 "In Proof B.2 (Proof of ()) . ‣ On condition (b): when does the model law admit a density? ‣ B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")), the directional derivative in the direction
Δ​θ\Delta\theta is

|  |  |  |  |
| --- | --- | --- | --- |
|  | dd​ϵ​𝒟​(pθϵ,pr)|ϵ=0=⟨𝔼𝐳​[[Jθ​Gθ​(𝐳,𝐜)]⊤​∇𝐱ψ​(Gθ​(𝐳,𝐜))],Δ​θ⟩.\frac{d}{d\epsilon}\mathcal{D}(p\_{\theta\_{\epsilon}},p\_{r})\bigg|\_{\epsilon=0}=\left\langle\mathbb{E}\_{\mathbf{z}}\left[\bigl[J\_{\theta}G\_{\theta}(\mathbf{z},\mathbf{c})\bigr]^{\top}\nabla\_{\mathbf{x}}\psi(G\_{\theta}(\mathbf{z},\mathbf{c}))\right],\Delta\theta\right\rangle. |  | (29) |

Since Δ​θ\Delta\theta is arbitrary,

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇θ𝒟​(pθ,pr)=𝔼𝐳​[[Jθ​Gθ​(𝐳,𝐜)]⊤​∇𝐱ψ​(Gθ​(𝐳,𝐜))⏟𝐠𝒟​(Gθ​(𝐳,𝐜))].\nabla\_{\theta}\mathcal{D}(p\_{\theta},p\_{r})=\mathbb{E}\_{\mathbf{z}}\left[\bigl[J\_{\theta}G\_{\theta}(\mathbf{z},\mathbf{c})\bigr]^{\top}\underbrace{\nabla\_{\mathbf{x}}\psi(G\_{\theta}(\mathbf{z},\mathbf{c}))}\_{\mathbf{g}\_{\mathcal{D}}(G\_{\theta}(\mathbf{z},\mathbf{c}))}\right]. |  | (30) |

Thus the sample-space distribution gradient in ([5](#S3.E5 "In 3.2 Parameter Gradient ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching")) is
𝐠𝒟​(𝐱)=∇𝐱ψ​(𝐱)\mathbf{g}\_{\mathcal{D}}(\mathbf{x})=\nabla\_{\mathbf{x}}\psi(\mathbf{x}) whenever the discrepancy admits the first variation ψ=δ​𝒟​(pθ,pr)/δ​pθ\psi=\delta\mathcal{D}(p\_{\theta},p\_{r})/\delta p\_{\theta}.

#### B.1.2 ff-divergence specialization

Here ρ⁡(𝐱):=pθ​(𝐱)/pr​(𝐱)\rho(\mathbf{x}):=p\_{\theta}(\mathbf{x})/p\_{r}(\mathbf{x}) denotes the density ratio.

The following template is the ff-divergence distribution-matching result of [Xu et al. (2025)](#bib.bib68), whose variational form goes back to ff-GAN ([Nowozin et al., 2016](#bib.bib58)).
We restate it in the present notation, and add in [Appendix B.1.3](#A2.SS1.SSS3 "B.1.3 Important special cases ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching") the distinction between an identified ff-divergence first variation and a detached optimal-discriminator update field, which the two coincide on only for particular generators.

###### Theorem B.3 (Unified Gradient Template for ff-divergences) .

Let Gθ​(𝐳,𝐜)=𝐱G\_{\theta}(\mathbf{z},\mathbf{c})=\mathbf{x} be the generator at fixed 𝐜\mathbf{c} and h:(0,∞)→ℝh:(0,\infty)\to\mathbb{R} be a twice continuously differentiable convex divergence generator with
h⁡(1)=0h(1)=0, and define

|  |  |  |  |
| --- | --- | --- | --- |
|  | Dh(pθ∥pr)=∫pr(𝐱)h(ρ(𝐱))d𝐱,ρ(𝐱):=pθ​(𝐱)pr​(𝐱).D\_{h}(p\_{\theta}\|p\_{r})=\int p\_{r}(\mathbf{x})h(\rho(\mathbf{x}))\,\mathrm{d}\mathbf{x},\qquad\rho(\mathbf{x}):=\frac{p\_{\theta}(\mathbf{x})}{p\_{r}(\mathbf{x})}. |  | (31) |

Assume [Assump. 1](#Thminnerassumption1 "Assumption 1 (Regularity for the first variation) . ‣ B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching") applies to
ℒ[pθ]=Dh(pθ∥pr)\mathcal{L}[p\_{\theta}]=D\_{h}(p\_{\theta}\|p\_{r}), and assume pθp\_{\theta} and prp\_{r} are smooth and strictly positive on an open set containing supp⁡(pθ)\operatorname{supp}(p\_{\theta}). Then the distribution gradient is

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐠h​(𝐱)=h′′​(ρ⁡(𝐱))​ρ​(𝐱)​(𝐬θ​(𝐱)−𝐬r​(𝐱)),\mathbf{g}\_{h}(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\,\rho(\mathbf{x})\,(\mathbf{s}\_{\theta}(\mathbf{x})-\mathbf{s}\_{r}(\mathbf{x})), |  | (32) |

and

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇θDh(pθ∥pr)=𝔼𝐳∼pz[[JθGθ(𝐳,𝐜)]⊤[w(𝐱)(𝐬θ(𝐱)−𝐬r(𝐱))]𝐱=Gθ​(𝐳,𝐜)],\nabla\_{\theta}D\_{h}(p\_{\theta}\|p\_{r})={\mathbb{E}}\_{\mathbf{z}\sim p\_{z}}\left[\bigl[J\_{\theta}G\_{\theta}(\mathbf{z},\mathbf{c})\bigr]^{\top}\left[w(\mathbf{x})(\mathbf{s}\_{\theta}(\mathbf{x})-\mathbf{s}\_{r}(\mathbf{x}))\right]\_{\mathbf{x}=G\_{\theta}(\mathbf{z},\mathbf{c})}\right], |  | (33) |

where w⁡(𝐱)=h′′​(ρ⁡(𝐱))​ρ​(𝐱)w(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\rho(\mathbf{x}).

###### Proof B.4 .

We first compute the first variation with respect to the model density pθp\_{\theta}, while keeping prp\_{r} fixed. Let pϵ=pθ+ϵ​δ​pp\_{\epsilon}=p\_{\theta}+\epsilon\,\delta p be an admissible smooth perturbation with ∫δ​p​(𝐱)​𝑑𝐱=0\int\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x}=0, and define ρϵ​(𝐱):=pϵ​(𝐱)/pr​(𝐱)\rho\_{\epsilon}(\mathbf{x}):=p\_{\epsilon}(\mathbf{x})/p\_{r}(\mathbf{x}). Since prp\_{r} is fixed, we have

|  |  |  |  |
| --- | --- | --- | --- |
|  | ρϵ​(𝐱)=ρ⁡(𝐱)+ϵ​δ​p​(𝐱)pr​(𝐱).\rho\_{\epsilon}(\mathbf{x})=\rho(\mathbf{x})+\epsilon\,\frac{\delta p(\mathbf{x})}{p\_{r}(\mathbf{x})}. |  | (34) |

Therefore the derivative is

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | dd​ϵDh(pϵ∥pr)|ϵ=0\displaystyle\frac{d}{d\epsilon}D\_{h}(p\_{\epsilon}\|p\_{r})\bigg|\_{\epsilon=0} | =∫pr​(𝐱)​[dd​ϵ​h​(ρϵ​(𝐱))|ϵ=0]​𝑑𝐱\displaystyle=\int p\_{r}(\mathbf{x})\,\left[\frac{d}{d\epsilon}h\left(\rho\_{\epsilon}(\mathbf{x})\right)\bigg|\_{\epsilon=0}\,\right]\,\mathrm{d}\mathbf{x} |  | (35) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =∫pr​(𝐱)​[dd​ϵ​h​(ρ⁡(𝐱)+ϵ​δ​p​(𝐱)pr​(𝐱))|ϵ=0]​𝑑𝐱\displaystyle=\int p\_{r}(\mathbf{x})\,\left[\frac{d}{d\epsilon}h\left(\rho(\mathbf{x})+\epsilon\,\frac{\delta p(\mathbf{x})}{p\_{r}(\mathbf{x})}\right)\bigg|\_{\epsilon=0}\,\right]\,\mathrm{d}\mathbf{x} |  | (36) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =∫pr​(𝐱)​h′​(ρ⁡(𝐱))​δ​p​(𝐱)pr​(𝐱)​𝑑𝐱\displaystyle=\int p\_{r}(\mathbf{x})\,h^{\prime}(\rho(\mathbf{x}))\,\frac{\delta p(\mathbf{x})}{p\_{r}(\mathbf{x})}\,\mathrm{d}\mathbf{x} |  | (37) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =∫h′​(ρ⁡(𝐱))​δ​p​(𝐱)​𝑑𝐱.\displaystyle=\int h^{\prime}(\rho(\mathbf{x}))\,\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x}\,. |  | (38) |

By definition, the first-variation potential is any function ψh\psi\_{h} whose pairing with every admissible density perturbation δ​p\delta p gives the directional derivative:

|  |  |  |  |
| --- | --- | --- | --- |
|  | dd​ϵDh(pθ+ϵδp∥pr)|ϵ=0=∫ψh(𝐱)δp(𝐱)d𝐱.\frac{d}{d\epsilon}D\_{h}(p\_{\theta}+\epsilon\,\delta p\|p\_{r})\bigg|\_{\epsilon=0}=\int\psi\_{h}(\mathbf{x})\,\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x}. |  | (39) |

Comparing this defining identity ([39](#A2.E39 "In Proof B.4 . ‣ B.1.2 𝑓-divergence specialization ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) with ([38](#A2.E38 "In Proof B.4 . ‣ B.1.2 𝑓-divergence specialization ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")), we can identify

|  |  |  |  |
| --- | --- | --- | --- |
|  | ψh​(𝐱):=δ​Dhδ​pθ​(𝐱)=h′​(ρ⁡(𝐱)).\psi\_{h}(\mathbf{x}):=\frac{\delta D\_{h}}{\delta p\_{\theta}}(\mathbf{x})=h^{\prime}(\rho(\mathbf{x})). |  | (40) |

This identification is unique up to an additive constant on the support of admissible perturbations, because ∫δ​p​(𝐱)​𝑑𝐱=0\int\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x}=0 and

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∫(ψh​(𝐱)+c0)​δ​p​(𝐱)​𝑑𝐱=∫ψh​(𝐱)​δ​p​(𝐱)​𝑑𝐱\int\bigl(\psi\_{h}(\mathbf{x})+c\_{0}\bigr)\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x}=\int\psi\_{h}(\mathbf{x})\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x} |  | (41) |

for any scalar constant c0c\_{0} (distinct from the conditioning vector 𝐜\mathbf{c}).

We now compute the sample-space field. By the chain rule,

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇𝐱ψh​(𝐱)=h′′​(ρ⁡(𝐱))​∇𝐱ρ​(𝐱).\nabla\_{\mathbf{x}}\psi\_{h}(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\nabla\_{\mathbf{x}}\rho(\mathbf{x}). |  | (42) |

It remains to express ∇𝐱ρ\nabla\_{\mathbf{x}}\rho in terms of the two scores. Since ρ=pθ/pr\rho=p\_{\theta}/p\_{r} and both densities are positive,

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇𝐱ρ​(𝐱)=∇𝐱pθ​(𝐱)pr​(𝐱)−pθ​(𝐱)​∇𝐱pr​(𝐱)pr​(𝐱)2.\nabla\_{\mathbf{x}}\rho(\mathbf{x})=\frac{\nabla\_{\mathbf{x}}p\_{\theta}(\mathbf{x})}{p\_{r}(\mathbf{x})}-\frac{p\_{\theta}(\mathbf{x})\nabla\_{\mathbf{x}}p\_{r}(\mathbf{x})}{p\_{r}(\mathbf{x})^{2}}. |  | (43) |

Using ∇𝐱pθ=pθ​𝐬θ\nabla\_{\mathbf{x}}p\_{\theta}=p\_{\theta}\mathbf{s}\_{\theta} and ∇𝐱pr=pr​𝐬r\nabla\_{\mathbf{x}}p\_{r}=p\_{r}\mathbf{s}\_{r}, this becomes

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇𝐱ρ​(𝐱)\displaystyle\nabla\_{\mathbf{x}}\rho(\mathbf{x}) | =pθ​(𝐱)​𝐬θ​(𝐱)pr​(𝐱)−pθ​(𝐱)​pr​(𝐱)​𝐬r​(𝐱)pr​(𝐱)2\displaystyle=\frac{p\_{\theta}(\mathbf{x})\mathbf{s}\_{\theta}(\mathbf{x})}{p\_{r}(\mathbf{x})}-\frac{p\_{\theta}(\mathbf{x})p\_{r}(\mathbf{x})\mathbf{s}\_{r}(\mathbf{x})}{p\_{r}(\mathbf{x})^{2}} |  |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =ρ⁡(𝐱)​(𝐬θ​(𝐱)−𝐬r​(𝐱)).\displaystyle=\rho(\mathbf{x})\bigl(\mathbf{s}\_{\theta}(\mathbf{x})-\mathbf{s}\_{r}(\mathbf{x})\bigr). |  | (44) |

Substituting this identity into ([42](#A2.E42 "In Proof B.4 . ‣ B.1.2 𝑓-divergence specialization ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) gives

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇𝐱ψh​(𝐱)=h′′​(ρ⁡(𝐱))​ρ​(𝐱)​(𝐬θ​(𝐱)−𝐬r​(𝐱)).\nabla\_{\mathbf{x}}\psi\_{h}(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\,\rho(\mathbf{x})(\mathbf{s}\_{\theta}(\mathbf{x})-\mathbf{s}\_{r}(\mathbf{x})). |  | (45) |

Therefore the distribution gradient is

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐠h​(𝐱)=∇𝐱ψh​(𝐱)=h′′​(ρ⁡(𝐱))​ρ​(𝐱)​(𝐬θ​(𝐱)−𝐬r​(𝐱)).\mathbf{g}\_{h}(\mathbf{x})=\nabla\_{\mathbf{x}}\psi\_{h}(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\,\rho(\mathbf{x})(\mathbf{s}\_{\theta}(\mathbf{x})-\mathbf{s}\_{r}(\mathbf{x})). |  | (46) |

Finally, applying the general first-variation template ([30](#A2.E30 "In Proof B.2 (Proof of ()) . ‣ On condition (b): when does the model law admit a density? ‣ B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) to ℒ[pθ]=Dh(pθ∥pr)\mathcal{L}[p\_{\theta}]=D\_{h}(p\_{\theta}\|p\_{r}) yields

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇θDh(pθ∥pr)\displaystyle\nabla\_{\theta}D\_{h}(p\_{\theta}\|p\_{r}) | =𝔼𝐳∼pz​[[Jθ​Gθ​(𝐳,𝐜)]⊤​𝐠h​(Gθ​(𝐳,𝐜))]\displaystyle={\mathbb{E}}\_{\mathbf{z}\sim p\_{z}}\left[\bigl[J\_{\theta}G\_{\theta}(\mathbf{z},\mathbf{c})\bigr]^{\top}\mathbf{g}\_{h}(G\_{\theta}(\mathbf{z},\mathbf{c}))\right] |  |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =𝔼𝐳∼pz​[[Jθ​Gθ​(𝐳,𝐜)]⊤​[h′′​(ρ⁡(𝐱))​ρ​(𝐱)​(𝐬θ​(𝐱)−𝐬r​(𝐱))]𝐱=Gθ​(𝐳,𝐜)].\displaystyle={\mathbb{E}}\_{\mathbf{z}\sim p\_{z}}\left[\bigl[J\_{\theta}G\_{\theta}(\mathbf{z},\mathbf{c})\bigr]^{\top}\left[h^{\prime\prime}(\rho(\mathbf{x}))\,\rho(\mathbf{x})(\mathbf{s}\_{\theta}(\mathbf{x})-\mathbf{s}\_{r}(\mathbf{x}))\right]\_{\mathbf{x}=G\_{\theta}(\mathbf{z},\mathbf{c})}\right]. |  | (47) |

With w⁡(𝐱)=h′′​(ρ⁡(𝐱))​ρ​(𝐱)w(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\rho(\mathbf{x}), this is exactly
([33](#A2.E33 "In Theorem B.3 (Unified Gradient Template for 𝑓-divergences) . ‣ B.1.2 𝑓-divergence specialization ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")).

#### B.1.3 Important special cases

The density-ratio-weighted form w⁡(𝐱)​(𝐬θ−𝐬r)w(\mathbf{x})(\mathbf{s}\_{\theta}-\mathbf{s}\_{r}) with w=h′′​(ρ)​ρw=h^{\prime\prime}(\rho)\rho is the one-step ff-divergence template of [Xu et al. (2025)](#bib.bib68), later extended to broader divergence families by [Wang et al. (2026)](#bib.bib69); reading the optimal-discriminator field of GANs as a weighted score difference follows [Yi et al. (2023)](#bib.bib75).

##### Reverse KL / DMD.

For h⁡(ρ)=ρ​log⁡ρh(\rho)=\rho\log\rho, we have h′′​(ρ)=1/ρh^{\prime\prime}(\rho)=1/\rho, hence w=ρ​h′′​(ρ)=1w=\rho h^{\prime\prime}(\rho)=1.
The distribution gradient is therefore

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐠KL​(𝐱)=𝐬θ​(𝐱)−𝐬r​(𝐱).\mathbf{g}\_{\mathrm{KL}}(\mathbf{x})=\mathbf{s}\_{\theta}(\mathbf{x})-\mathbf{s}\_{r}(\mathbf{x}). |  | (48) |

This is the ideal reverse-KL field; the score-difference component of practical DMD estimates its noisy-marginal counterpart with approximate reference and online fake score models.
It is not the complete DMD objective: the original method also uses an LPIPS regression term on pre-generated teacher pairs, and its finite-training online fake-score estimate can be lagged or biased ([Yin et al., 2024b](#bib.bib16)).
The corresponding sample-space descent direction is −𝐠KL=𝐬r−𝐬θ-\mathbf{g}\_{\mathrm{KL}}=\mathbf{s}\_{r}-\mathbf{s}\_{\theta}.

##### Scaled Jensen–Shannon / saturating GAN.

Using twice the conventional equal-mixture JSD generator (the scale is chosen to match the saturating GAN field),

|  |  |  |  |
| --- | --- | --- | --- |
|  | hJSD​(ρ)=ρ​log⁡ρ−(1+ρ)​log⁡1+ρ2,h\_{\mathrm{JSD}}(\rho)=\rho\log\rho-(1+\rho)\log\frac{1+\rho}{2}, |  | (49) |

we have

|  |  |  |  |
| --- | --- | --- | --- |
|  | hJSD′′​(ρ)=1ρ⁡(1+ρ),wJSD​(ρ)=11+ρ=D∗​(𝐱),h\_{\mathrm{JSD}}^{\prime\prime}(\rho)=\frac{1}{\rho(1+\rho)},\qquad w\_{\mathrm{JSD}}(\rho)=\frac{1}{1+\rho}=D^{\*}(\mathbf{x}), |  | (50) |

where D∗​(𝐱)=pr/(pr+pθ)D^{\*}(\mathbf{x})=p\_{r}/(p\_{r}+p\_{\theta}) is the optimal real-probability discriminator ([Goodfellow et al., 2014](#bib.bib4)) (here the superscript ∗ denotes optimality, distinct from its use for exact marginal velocity fields elsewhere).

##### Detached optimal discriminator generator updates.

Assume smooth positive densities and an exact optimal discriminator.
We hold the discriminator parameters fixed while retaining derivatives with respect to its input.
Under D∗​(𝐱)=pr/(pr+pθ)D^{\*}(\mathbf{x})=p\_{r}/(p\_{r}+p\_{\theta}), we have 1−D∗=pθ/(pr+pθ)1{-}D^{\*}=p\_{\theta}/(p\_{r}+p\_{\theta}).
For the saturating objective ℓsat​(𝐱)=log⁡(1−D∗​(𝐱))=log⁡pθ−log⁡(pr+pθ)\ell\_{\mathrm{sat}}(\mathbf{x})=\log(1{-}D^{\*}(\mathbf{x}))=\log p\_{\theta}-\log(p\_{r}+p\_{\theta}):

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇𝐱ℓsat​(𝐱)\displaystyle\nabla\_{\mathbf{x}}\ell\_{\mathrm{sat}}(\mathbf{x}) | =𝐬θ​(𝐱)−pr​𝐬r​(𝐱)+pθ​𝐬θ​(𝐱)pr+pθ\displaystyle=\mathbf{s}\_{\theta}(\mathbf{x})-\frac{p\_{r}\,\mathbf{s}\_{r}(\mathbf{x})+p\_{\theta}\,\mathbf{s}\_{\theta}(\mathbf{x})}{p\_{r}+p\_{\theta}} |  |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =𝐬θ−D∗​𝐬r−(1−D∗)​𝐬θ=D∗​(𝐱)​(𝐬θ​(𝐱)−𝐬r​(𝐱)).\displaystyle=\mathbf{s}\_{\theta}-D^{\*}\mathbf{s}\_{r}-(1{-}D^{\*})\mathbf{s}\_{\theta}=D^{\*}(\mathbf{x})(\mathbf{s}\_{\theta}(\mathbf{x})-\mathbf{s}\_{r}(\mathbf{x}))\,. |  | (51) |

For the non-saturating objective ℓns​(𝐱)=−log⁡D∗​(𝐱)=log⁡(pr+pθ)−log⁡pr\ell\_{\mathrm{ns}}(\mathbf{x})=-\log D^{\*}(\mathbf{x})=\log(p\_{r}+p\_{\theta})-\log p\_{r}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇𝐱ℓns​(𝐱)\displaystyle\nabla\_{\mathbf{x}}\ell\_{\mathrm{ns}}(\mathbf{x}) | =pr​𝐬r​(𝐱)+pθ​𝐬θ​(𝐱)pr+pθ−𝐬r​(𝐱)\displaystyle=\frac{p\_{r}\,\mathbf{s}\_{r}(\mathbf{x})+p\_{\theta}\,\mathbf{s}\_{\theta}(\mathbf{x})}{p\_{r}+p\_{\theta}}-\mathbf{s}\_{r}(\mathbf{x}) |  |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =D∗​𝐬r+(1−D∗)​𝐬θ−𝐬r=(1−D∗​(𝐱))​(𝐬θ​(𝐱)−𝐬r​(𝐱)).\displaystyle=D^{\*}\mathbf{s}\_{r}+(1{-}D^{\*})\mathbf{s}\_{\theta}-\mathbf{s}\_{r}=(1{-}D^{\*}(\mathbf{x}))(\mathbf{s}\_{\theta}(\mathbf{x})-\mathbf{s}\_{r}(\mathbf{x}))\,. |  | (52) |

The saturating field agrees with the distribution gradient of the scaled JSD above; the non-saturating field is instead a detached-optimal-discriminator generator update.

##### Special cases.

|  |  |  |  |
| --- | --- | --- | --- |
| Objective / divergence | h⁡(ρ)h(\rho) | h′′​(ρ)h^{\prime\prime}(\rho) | w=h′′​(ρ)⋅ρw=h^{\prime\prime}(\rho)\cdot\rho |
| Reverse KL (DMD) | ρ​log⁡ρ\rho\log\rho | 1/ρ1/\rho | 11 |
| Scaled JSD (2×\timesJSD) | ρ​log⁡ρ−(1+ρ)​log⁡1+ρ2\rho\log\rho-(1{+}\rho)\log\frac{1{+}\rho}{2} | 1ρ⁡(1+ρ)\frac{1}{\rho(1{+}\rho)} | 11+ρ=D∗\frac{1}{1{+}\rho}=D^{\*} |
| NS-GAN detached update | —† | — | 1−D∗1-D^{\*} |
| Saturating GAN | scaled JSD above | as above | D∗D^{\*} |

Here † denotes only the detached optimal-D∗D^{\*} generator update field, not an identified ff-divergence first variation; the saturating-GAN row is the scaled 2×2{\times}JSD field in the preceding row.

### B.2 Score Decomposition of the Reverse-KL Field

#### B.2.1 Score Decomposition Identity

###### Definition B.5 (Moment-Matched Gaussian) .

For any distribution pp over ℝd\mathbb{R}^{d} with finite first and second moments and positive-definite covariance, define its *moment-matched Gaussian* as

|  |  |  |  |
| --- | --- | --- | --- |
|  | qp:=𝒩⁡(μp,Σp),μp:=𝔼p​[𝐱],Σp:=Covp⁡(𝐱).q\_{p}:=\mathcal{N}(\mu\_{p},\Sigma\_{p})\,,\qquad\mu\_{p}:=\mathbb{E}\_{p}[\mathbf{x}]\,,\quad\Sigma\_{p}:=\operatorname{Cov}\_{p}(\mathbf{x})\,. |  | (53) |

###### Definition B.6 (Non-Gaussian Score Residual) .

For any smooth distribution pp satisfying [Def. B.5](#A2.Thmtheorem5 "Definition B.5 (Moment-Matched Gaussian) . ‣ B.2.1 Score Decomposition Identity ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"), with score 𝐬p​(𝐱)=∇𝐱​log​p​(𝐱)\mathbf{s}\_{p}(\mathbf{x})=\nabla\_{\mathbf{x}}\log p(\mathbf{x}) and moment-matched Gaussian qpq\_{p}, define the non-Gaussian score residual as

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝜼p​(𝐱):=𝐬p​(𝐱)−𝐬qp​(𝐱).\bm{\eta}\_{p}(\mathbf{x}):=\mathbf{s}\_{p}(\mathbf{x})-\mathbf{s}\_{q\_{p}}(\mathbf{x})\,. |  | (54) |

where 𝐬qp​(𝐱)=−Σp−1​(𝐱−μp)\mathbf{s}\_{q\_{p}}(\mathbf{x})=-\Sigma\_{p}^{-1}(\mathbf{x}-\mu\_{p}).

Therefore, based on [Def. B.5](#A2.Thmtheorem5 "Definition B.5 (Moment-Matched Gaussian) . ‣ B.2.1 Score Decomposition Identity ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching") and [Def. B.6](#A2.Thmtheorem6 "Definition B.6 (Non-Gaussian Score Residual) . ‣ B.2.1 Score Decomposition Identity ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"), we can decompose the score function of any distribution pp as

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐬p​(𝐱)=𝐬qp​(𝐱)+𝜼p​(𝐱).\mathbf{s}\_{p}(\mathbf{x})=\mathbf{s}\_{q\_{p}}(\mathbf{x})+\bm{\eta}\_{p}(\mathbf{x})\,. |  | (55) |

This is the *score decomposition* in Eq. [6](#S3.E6 "In 3.3 Decomposition of the Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching") of the main text.

#### B.2.2 Orthogonality of the Residual

We use the following scalar-test-function form of Stein’s identity ([Liu et al., 2016](#bib.bib70), Def. 2.1 and Lem. 2.2). If φ:ℝd→ℝ\varphi:\mathbb{R}^{d}\to\mathbb{R} belongs to the Stein class of pp, then

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝐬p​(𝐱)​φ​(𝐱)+∇𝐱φ​(𝐱)]=𝟎.\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})\varphi(\mathbf{x})+\nabla\_{\mathbf{x}}\varphi(\mathbf{x})]=\mathbf{0}. |  | (56) |

The two identities in [Lem. B.7](#A2.Thmtheorem7 "Lemma B.7 (Score Stein Identities) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching") correspond to φ⁡(𝐱)=1\varphi(\mathbf{x})=1 and φ⁡(𝐱)=xl\varphi(\mathbf{x})=x\_{l}. We include a coordinate proof for clarity.

###### Lemma B.7 (Score Stein Identities) .

Let pp be a strictly positive smooth density on ℝd\mathbb{R}^{d} with score
𝐬p​(𝐱)=∇𝐱​log​p​(𝐱)\mathbf{s}\_{p}(\mathbf{x})=\nabla\_{\mathbf{x}}\log p(\mathbf{x}). Assume

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[‖𝐬p​(𝐱)‖]<∞,𝔼p​[‖𝐱‖​‖𝐬p​(𝐱)‖]<∞.\mathbb{E}\_{p}[\|\mathbf{s}\_{p}(\mathbf{x})\|]<\infty,\qquad\mathbb{E}\_{p}[\|\mathbf{x}\|\,\|\mathbf{s}\_{p}(\mathbf{x})\|]<\infty. |  | (57) |

For BR={𝐱:‖𝐱‖≤R}B\_{R}=\{\mathbf{x}:\|\mathbf{x}\|\leq R\}, let nkn\_{k} be the kk-th coordinate of the outward unit normal on ∂BR\partial B\_{R}.
Assume also that the following boundary condition holds for all coordinates (k,l)(k,l):

|  |  |  |  |
| --- | --- | --- | --- |
|  | limR→∞∫∂BRp⁡(𝐱)​nk​𝑑S=0,limR→∞∫∂BRp⁡(𝐱)​xl​nk​𝑑S=0.\lim\_{R\to\infty}\int\_{\partial B\_{R}}p(\mathbf{x})n\_{k}\,\mathrm{d}S=0,\qquad\lim\_{R\to\infty}\int\_{\partial B\_{R}}p(\mathbf{x})x\_{l}n\_{k}\,\mathrm{d}S=0. |  | (58) |

Then

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝐬p​(𝐱)]=𝟎,𝔼p​[𝐬p​(𝐱)​𝐱⊤]=−𝐈d.\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})]=\mathbf{0},\qquad\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})\mathbf{x}^{\top}]=-\mathbf{I}\_{d}. |  | (59) |

###### Proof B.8 .

Since p⁡(𝐱)​𝐬p​(𝐱)=∇𝐱p​(𝐱)p(\mathbf{x})\mathbf{s}\_{p}(\mathbf{x})=\nabla\_{\mathbf{x}}p(\mathbf{x}), the kk-th coordinate of
𝔼p​[𝐬p​(𝐱)]\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})] is

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[[𝐬p​(𝐱)]k]=∫∂p⁡(𝐱)∂xk​𝑑𝐱.\mathbb{E}\_{p}[[\mathbf{s}\_{p}(\mathbf{x})]\_{k}]=\int\frac{\partial p(\mathbf{x})}{\partial x\_{k}}\,\mathrm{d}\mathbf{x}. |  | (60) |

By the divergence theorem on BRB\_{R},

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∫BR∂p⁡(𝐱)∂xk​𝑑𝐱=∫∂BRp⁡(𝐱)​nk​𝑑S.\int\_{B\_{R}}\frac{\partial p(\mathbf{x})}{\partial x\_{k}}\,\mathrm{d}\mathbf{x}=\int\_{\partial B\_{R}}p(\mathbf{x})n\_{k}\,\mathrm{d}S. |  | (61) |

By ([57](#A2.E57 "In Lemma B.7 (Score Stein Identities) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")), the volume integrand is absolutely integrable. Taking R→∞R\to\infty and using the first limit in ([58](#A2.E58 "In Lemma B.7 (Score Stein Identities) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) gives

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∫∂p⁡(𝐱)∂xk​𝑑𝐱=0.\int\frac{\partial p(\mathbf{x})}{\partial x\_{k}}\,\mathrm{d}\mathbf{x}=0. |  | (62) |

Since this holds for every kk,

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝐬p​(𝐱)]=𝟎.\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})]=\mathbf{0}. |  | (63) |

For the second identity, fix coordinates (k,l)(k,l). Again by the divergence theorem,

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∫BR∂∂xk​[p⁡(𝐱)​xl]​𝑑𝐱=∫∂BRp⁡(𝐱)​xl​nk​𝑑S.\int\_{B\_{R}}\frac{\partial}{\partial x\_{k}}\!\left[p(\mathbf{x})x\_{l}\right]\,\mathrm{d}\mathbf{x}=\int\_{\partial B\_{R}}p(\mathbf{x})x\_{l}n\_{k}\,\mathrm{d}S. |  | (64) |

The second condition in ([57](#A2.E57 "In Lemma B.7 (Score Stein Identities) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) makes the expanded derivative integrable. Taking R→∞R\to\infty and using the second limit in ([58](#A2.E58 "In Lemma B.7 (Score Stein Identities) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) gives

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∫∂∂xk​[p⁡(𝐱)​xl]​𝑑𝐱=0.\int\frac{\partial}{\partial x\_{k}}\!\left[p(\mathbf{x})x\_{l}\right]\,\mathrm{d}\mathbf{x}=0. |  | (65) |

Expanding the derivative gives

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∂∂xk​[p⁡(𝐱)​xl]=∂p⁡(𝐱)∂xk​xl+p⁡(𝐱)​δk​l=p⁡(𝐱)​[𝐬p​(𝐱)]k​xl+p⁡(𝐱)​δk​l,\frac{\partial}{\partial x\_{k}}\!\left[p(\mathbf{x})x\_{l}\right]=\frac{\partial p(\mathbf{x})}{\partial x\_{k}}x\_{l}+p(\mathbf{x})\delta\_{kl}=p(\mathbf{x})[\mathbf{s}\_{p}(\mathbf{x})]\_{k}x\_{l}+p(\mathbf{x})\delta\_{kl}, |  | (66) |

where δk​l\delta\_{kl} is the Kronecker delta. Integrating and using ∫p⁡(𝐱)​𝑑𝐱=1\int p(\mathbf{x})\,\mathrm{d}\mathbf{x}=1 yields

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[[𝐬p​(𝐱)]k​xl]+δk​l=0.\mathbb{E}\_{p}\!\left[[\mathbf{s}\_{p}(\mathbf{x})]\_{k}x\_{l}\right]+\delta\_{kl}=0. |  | (67) |

Thus 𝔼p​[[𝐬p​(𝐱)]k​xl]=−δk​l\mathbb{E}\_{p}[[\mathbf{s}\_{p}(\mathbf{x})]\_{k}x\_{l}]=-\delta\_{kl} for all (k,l)(k,l), or in matrix form,

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝐬p​(𝐱)​𝐱⊤]=−𝐈d.\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})\mathbf{x}^{\top}]=-\mathbf{I}\_{d}. |  | (68) |

###### Proposition B.9 (Orthogonality of the Non-Gaussian Score Residual) .

Let pp be a strictly positive smooth density on ℝd\mathbb{R}^{d} with finite second moment and positive-definite covariance Σp\Sigma\_{p}. Assume the integrability condition ([57](#A2.E57 "In Lemma B.7 (Score Stein Identities) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) and boundary condition ([58](#A2.E58 "In Lemma B.7 (Score Stein Identities) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")). Finite Fisher information together with the finite second moment is sufficient for ([57](#A2.E57 "In Lemma B.7 (Score Stein Identities) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) by Cauchy–Schwarz. Then the non-Gaussian score residual 𝛈p=𝐬p−𝐬qp\bm{\eta}\_{p}=\mathbf{s}\_{p}-\mathbf{s}\_{q\_{p}} satisfies

1. (i)

   𝔼p​[𝜼p​(𝐱)]=𝟎\mathbb{E}\_{p}[\bm{\eta}\_{p}(\mathbf{x})]=\mathbf{0}.
2. (ii)

   𝔼p​[𝜼p​(𝐱)​𝐱⊤]=𝟎d×d\mathbb{E}\_{p}[\bm{\eta}\_{p}(\mathbf{x})\mathbf{x}^{\top}]=\mathbf{0}\_{d\times d}.

###### Proof B.10 .

Step 1: Score Stein identities.
By [Lem. B.7](#A2.Thmtheorem7 "Lemma B.7 (Score Stein Identities) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"),

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝐬p​(𝐱)]=𝟎,𝔼p​[𝐬p​(𝐱)​𝐱⊤]=−𝐈d.\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})]=\mathbf{0},\qquad\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})\mathbf{x}^{\top}]=-\mathbf{I}\_{d}. |  | (69) |

Step 2: The moment-matched Gaussian has the same two identities under
pp.
By definition, the score of qp=𝒩⁡(μp,Σp)q\_{p}=\mathcal{N}(\mu\_{p},\Sigma\_{p}) is

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐬qp​(𝐱)=−Σp−1​(𝐱−μp).\mathbf{s}\_{q\_{p}}(\mathbf{x})=-\Sigma\_{p}^{-1}(\mathbf{x}-\mu\_{p}). |  | (70) |

Taking expectation under pp gives

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝐬qp​(𝐱)]=−Σp−1​(𝔼p​[𝐱]−μp)=𝟎.\mathbb{E}\_{p}[\mathbf{s}\_{q\_{p}}(\mathbf{x})]=-\Sigma\_{p}^{-1}\bigl(\mathbb{E}\_{p}[\mathbf{x}]-\mu\_{p}\bigr)=\mathbf{0}. |  | (71) |

For the first-moment identity,

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝐬qp​(𝐱)​𝐱⊤]\displaystyle\mathbb{E}\_{p}[\mathbf{s}\_{q\_{p}}(\mathbf{x})\mathbf{x}^{\top}] | =−Σp−1​𝔼p​[(𝐱−μp)​𝐱⊤]\displaystyle=-\Sigma\_{p}^{-1}\mathbb{E}\_{p}[(\mathbf{x}-\mu\_{p})\mathbf{x}^{\top}] |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | =−Σp−1​𝔼p​[(𝐱−μp)​((𝐱−μp)+μp)⊤]\displaystyle=-\Sigma\_{p}^{-1}\mathbb{E}\_{p}[(\mathbf{x}-\mu\_{p})((\mathbf{x}-\mu\_{p})+\mu\_{p})^{\top}] |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | =−Σp−1​(𝔼p​[(𝐱−μp)​(𝐱−μp)⊤]+𝔼p​[𝐱−μp]​μp⊤)\displaystyle=-\Sigma\_{p}^{-1}\left(\mathbb{E}\_{p}[(\mathbf{x}-\mu\_{p})(\mathbf{x}-\mu\_{p})^{\top}]+\mathbb{E}\_{p}[\mathbf{x}-\mu\_{p}]\mu\_{p}^{\top}\right) |  |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =−Σp−1​Σp=−𝐈d.\displaystyle=-\Sigma\_{p}^{-1}\Sigma\_{p}=-\mathbf{I}\_{d}\,. |  | (72) |

Step 3: Subtract the Gaussian identities from the true-score
identities.
Since 𝛈p=𝐬p−𝐬qp\bm{\eta}\_{p}=\mathbf{s}\_{p}-\mathbf{s}\_{q\_{p}}, the identities in
[Lem. B.7](#A2.Thmtheorem7 "Lemma B.7 (Score Stein Identities) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching") and Step 2 imply

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝜼p​(𝐱)]=𝔼p​[𝐬p​(𝐱)]−𝔼p​[𝐬qp​(𝐱)]=𝟎.\mathbb{E}\_{p}[\bm{\eta}\_{p}(\mathbf{x})]=\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})]-\mathbb{E}\_{p}[\mathbf{s}\_{q\_{p}}(\mathbf{x})]=\mathbf{0}. |  | (73) |

Similarly,

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝜼p​(𝐱)​𝐱⊤]=𝔼p​[𝐬p​(𝐱)​𝐱⊤]−𝔼p​[𝐬qp​(𝐱)​𝐱⊤]=−𝐈d−(−𝐈d)=𝟎d×d.\mathbb{E}\_{p}[\bm{\eta}\_{p}(\mathbf{x})\mathbf{x}^{\top}]=\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})\mathbf{x}^{\top}]-\mathbb{E}\_{p}[\mathbf{s}\_{q\_{p}}(\mathbf{x})\mathbf{x}^{\top}]=-\mathbf{I}\_{d}-(-\mathbf{I}\_{d})=\mathbf{0}\_{d\times d}. |  | (74) |

Finally, combining (i) and (ii) yields the equivalent centered form:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝜼p​(𝐱)​(𝐱−μp)⊤]=𝔼p​[𝜼p​(𝐱)​𝐱⊤]−𝔼p​[𝜼p​(𝐱)]​μp⊤=𝟎d×d.\mathbb{E}\_{p}[\bm{\eta}\_{p}(\mathbf{x})(\mathbf{x}-\mu\_{p})^{\top}]=\mathbb{E}\_{p}[\bm{\eta}\_{p}(\mathbf{x})\mathbf{x}^{\top}]-\mathbb{E}\_{p}[\bm{\eta}\_{p}(\mathbf{x})]\mu\_{p}^{\top}=\mathbf{0}\_{d\times d}. |  | (75) |

#### B.2.3 Reverse-KL Field Decomposition

###### Theorem B.11 (Reverse-KL Field Decomposition) .

Assume pθp\_{\theta} and prp\_{r} are strictly positive smooth densities satisfying [Def. B.5](#A2.Thmtheorem5 "Definition B.5 (Moment-Matched Gaussian) . ‣ B.2.1 Score Decomposition Identity ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"), and set qi:=qpiq\_{i}:=q\_{p\_{i}} and 𝛈i:=𝛈pi\bm{\eta}\_{i}:=\bm{\eta}\_{p\_{i}} for i∈{r,θ}i\in\{r,\theta\}. For the reverse-KL distribution gradient 𝐠KL​(𝐱)=𝐬θ​(𝐱)−𝐬r​(𝐱)\mathbf{g}\_{\mathrm{KL}}(\mathbf{x})=\mathbf{s}\_{\theta}(\mathbf{x})-\mathbf{s}\_{r}(\mathbf{x}),

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐠KL(𝐱)=(𝐬qθ​(𝐱)−𝐬qr​(𝐱))⏟𝐠KLG​(𝐱):Gaussian moment component+(𝜼θ​(𝐱)−𝜼r​(𝐱))⏟𝐠KLnG​(𝐱):non-Gaussian residual component\mathbf{g}\_{\mathrm{KL}}(\mathbf{x})=\underbrace{\left(\mathbf{s}\_{q\_{\theta}}(\mathbf{x})-\mathbf{s}\_{q\_{r}}(\mathbf{x})\right)}\_{\mathbf{g}\_{\mathrm{KL}}^{\mathrm{G}}(\mathbf{x}):\;\text{Gaussian moment component}}+\underbrace{\left(\bm{\eta}\_{\theta}(\mathbf{x})-\bm{\eta}\_{r}(\mathbf{x})\right)}\_{\mathbf{g}\_{\mathrm{KL}}^{\mathrm{nG}}(\mathbf{x}):\;\text{non-Gaussian residual component}} |  | (76) |

where 𝐠KLG​(𝐱)=−Σθ−1​(𝐱−μθ)+Σr−1​(𝐱−μr)\mathbf{g}\_{\mathrm{KL}}^{\mathrm{G}}(\mathbf{x})=-\Sigma\_{\theta}^{-1}(\mathbf{x}-\mu\_{\theta})+\Sigma\_{r}^{-1}(\mathbf{x}-\mu\_{r}) depends only on the first two moments, and 𝐠KLnG​(𝐱)=𝛈θ​(𝐱)−𝛈r​(𝐱)\mathbf{g}\_{\mathrm{KL}}^{\mathrm{nG}}(\mathbf{x})=\bm{\eta}\_{\theta}(\mathbf{x})-\bm{\eta}\_{r}(\mathbf{x}) captures the remaining score structure.
This exact decomposition is stated for the unweighted reverse-KL field. For a general ff-divergence field w⁡(𝐱)​(𝐬θ−𝐬r)w(\mathbf{x})(\mathbf{s}\_{\theta}-\mathbf{s}\_{r}), the algebraic decomposition is multiplied by w⁡(𝐱)w(\mathbf{x}), but the residual orthogonality identities need not be preserved after weighting.

###### Proof B.12 .

Apply the score decomposition in ([55](#A2.E55 "In B.2.1 Score Decomposition Identity ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"))
to both 𝐬θ\mathbf{s}\_{\theta} and 𝐬r\mathbf{s}\_{r}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐬θ​(𝐱)−𝐬r​(𝐱)\displaystyle\mathbf{s}\_{\theta}(\mathbf{x})-\mathbf{s}\_{r}(\mathbf{x}) | =[𝐬qθ​(𝐱)+𝜼θ​(𝐱)]−[𝐬qr​(𝐱)+𝜼r​(𝐱)]\displaystyle=\left[\mathbf{s}\_{q\_{\theta}}(\mathbf{x})+\bm{\eta}\_{\theta}(\mathbf{x})\right]-\left[\mathbf{s}\_{q\_{r}}(\mathbf{x})+\bm{\eta}\_{r}(\mathbf{x})\right] |  |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =(𝐬qθ​(𝐱)−𝐬qr​(𝐱))⏟𝐠KLG+(𝜼θ​(𝐱)−𝜼r​(𝐱))⏟𝐠KLnG.\displaystyle=\underbrace{\left(\mathbf{s}\_{q\_{\theta}}(\mathbf{x})-\mathbf{s}\_{q\_{r}}(\mathbf{x})\right)}\_{\mathbf{g}\_{\mathrm{KL}}^{\mathrm{G}}}+\underbrace{\left(\bm{\eta}\_{\theta}(\mathbf{x})-\bm{\eta}\_{r}(\mathbf{x})\right)}\_{\mathbf{g}\_{\mathrm{KL}}^{\mathrm{nG}}}\,. |  | (77) |

#### B.2.4 Diagonal Form and Connection to Estimators

In the diagonal case Σi=diag(σi,12,…,σi,d2)\Sigma\_{i}=\diag(\sigma\_{i,1}^{2},\ldots,\sigma\_{i,d}^{2}), where σi,j>0\sigma\_{i,j}>0 is the standard deviation of coordinate jj under pip\_{i} for i∈{r,θ}i\in\{r,\theta\},

|  |  |  |  |
| --- | --- | --- | --- |
|  | gKL,jG​(𝐱):=[𝐠KLG​(𝐱)]j=[−Σθ−1​(𝐱−μθ)+Σr−1​(𝐱−μr)]j=−xj−μθ,jσθ,j2+xj−μr,jσr,j2.g^{\mathrm{G}}\_{\mathrm{KL},j}(\mathbf{x}):=[\mathbf{g}\_{\mathrm{KL}}^{\mathrm{G}}(\mathbf{x})]\_{j}=[-\Sigma\_{\theta}^{-1}(\mathbf{x}-\mu\_{\theta})+\Sigma\_{r}^{-1}(\mathbf{x}-\mu\_{r})]\_{j}=-\frac{x\_{j}-\mu\_{\theta,j}}{\sigma\_{\theta,j}^{2}}+\frac{x\_{j}-\mu\_{r,j}}{\sigma\_{r,j}^{2}}\,. |  | (78) |

Requiring gKL,jG​(𝐱)=0g^{\mathrm{G}}\_{\mathrm{KL},j}(\mathbf{x})=0 for all 𝐱\mathbf{x} forces the coefficient of xjx\_{j} to vanish:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 1σr,j2−1σθ,j2=0⟹σθ,j=σr,j.\frac{1}{\sigma\_{r,j}^{2}}-\frac{1}{\sigma\_{\theta,j}^{2}}=0\;\;\Longrightarrow\;\;\sigma\_{\theta,j}=\sigma\_{r,j}\,. |  | (79) |

Substituting back into the constant term gives μθ,j=μr,j\mu\_{\theta,j}=\mu\_{r,j}.
In the same coordinate space, this is the fixed-point condition for diagonal Gaussian moment matching; Eq. [13](#S4.E13 "In Matching feature moments. ‣ 4.2 Feature-Moment Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching") imposes the analogous condition on pooled feature moments.
In ϕ\phi-space, the moment-matching gradient in [Prop. B.20](#A2.Thmtheorem20 "Proposition B.20 (Gradient of the Feature-Moment Loss) . ‣ Fixed-feature updates. ‣ B.6 Gradient of the Feature-Moment Loss ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching") defines a pooled feature-space regularizer motivated by 𝐠KLG\mathbf{g}\_{\mathrm{KL}}^{\mathrm{G}}.
At fixed feature-map parameters and queues, let 𝐡k=ϕθ¯​(𝐱k,𝐜k)\mathbf{h}\_{k}=\phi\_{\bar{\theta}}(\mathbf{x}\_{k},\mathbf{c}\_{k}) be a current model feature. Its empirical sample-gradient contribution is

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∂ℒ^pop∂𝐱k=[J𝐱​ϕθ¯​(𝐱k,𝐜k)]⊤​∂ℒ^pop∂𝐡k,\frac{\partial\widehat{\mathcal{L}}\_{\text{pop}}}{\partial\mathbf{x}\_{k}}=\bigl[J\_{\mathbf{x}}\phi\_{\bar{\theta}}(\mathbf{x}\_{k},\mathbf{c}\_{k})\bigr]^{\top}\frac{\partial\widehat{\mathcal{L}}\_{\text{pop}}}{\partial\mathbf{h}\_{k}}, |  | (80) |

where J𝐱​ϕθ¯:=∂ϕθ¯/∂𝐱J\_{\mathbf{x}}\phi\_{\bar{\theta}}:=\partial\phi\_{\bar{\theta}}/\partial\mathbf{x}, and the feature derivative is given in [Prop. B.20](#A2.Thmtheorem20 "Proposition B.20 (Gradient of the Feature-Moment Loss) . ‣ Fixed-feature updates. ‣ B.6 Gradient of the Feature-Moment Loss ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"). Thus the feature-moment loss is a pooled feature-space moment regularizer motivated by 𝐠KLG\mathbf{g}\_{\mathrm{KL}}^{\mathrm{G}}, not an estimate of it.

The internal velocity difference in the DMD loss in [Section 4.1](#S4.SS1 "4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching") yields an estimate of the full noisy reverse-KL field through Eq. [9](#S4.E9 "In 4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching"), including both moment and residual components.
The feature-moment loss adds an explicit constraint on pooled feature statistics alongside this pointwise signal.
Whether this signal has lower empirical gradient variance is an experimental question, not a consequence of the decomposition.

#### B.2.5 Variational characterization via L2L^{2} projection

The score decomposition ([6](#S3.E6 "In 3.3 Decomposition of the Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching")) admits a variational interpretation that explains why the moment-matched Gaussian is not an arbitrary choice but rather the unique optimal affine approximation.

Assume that pp satisfies the regularity conditions of [Prop. B.9](#A2.Thmtheorem9 "Proposition B.9 (Orthogonality of the Non-Gaussian Score Residual) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching") and additionally has finite Fisher information:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[‖𝐬p​(𝐱)‖2]=𝔼p​[‖∇𝐱​log​p​(𝐱)‖2]<∞.\mathbb{E}\_{p}[\|\mathbf{s}\_{p}(\mathbf{x})\|^{2}]=\mathbb{E}\_{p}[\|\nabla\_{\mathbf{x}}\log p(\mathbf{x})\|^{2}]<\infty. |  | (81) |

This ensures that the L2​(p)L^{2}(p) optimization problem below is well-posed.

Consider the problem of approximating the score function 𝐬p\mathbf{s}\_{p} by an affine function in L2​(p)L^{2}(p):

|  |  |  |  |
| --- | --- | --- | --- |
|  | min𝐀∈ℝd×d,𝐛∈ℝd⁡𝔼p​[‖𝐬p​(𝐱)−(𝐀𝐱+𝐛)‖2].\min\_{\mathbf{A}\in\mathbb{R}^{d\times d},\mathbf{b}\in\mathbb{R}^{d}}\;\mathbb{E}\_{p}[\|\mathbf{s}\_{p}(\mathbf{x})-(\mathbf{A}\mathbf{x}+\mathbf{b})\|^{2}]. |  | (82) |

The first-order optimality conditions (normal equations) for this least-squares problem are:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝔼p​[𝐬p​(𝐱)−(𝐀𝐱+𝐛)]\displaystyle\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})-(\mathbf{A}\mathbf{x}+\mathbf{b})] | =𝟎,\displaystyle=\mathbf{0}, |  | (83) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝔼p​[(𝐬p​(𝐱)−(𝐀𝐱+𝐛))​𝐱⊤]\displaystyle\mathbb{E}\_{p}[(\mathbf{s}\_{p}(\mathbf{x})-(\mathbf{A}\mathbf{x}+\mathbf{b}))\mathbf{x}^{\top}] | =𝟎.\displaystyle=\mathbf{0}. |  | (84) |

These are exactly the orthogonality conditions ([8](#S3.E8 "In 3.3 Decomposition of the Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching")).

To solve for 𝐀\mathbf{A} and 𝐛\mathbf{b}, expand the first condition:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[𝐬p​(𝐱)]=𝐀​𝔼p​[𝐱]+𝐛.\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})]=\mathbf{A}\mathbb{E}\_{p}[\mathbf{x}]+\mathbf{b}. |  | (85) |

By Stein’s identity in [Lem. B.7](#A2.Thmtheorem7 "Lemma B.7 (Score Stein Identities) . ‣ B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"), 𝔼p​[𝐬p​(𝐱)]=𝟎\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})]=\mathbf{0} and 𝔼p​[𝐱]=μp\mathbb{E}\_{p}[\mathbf{x}]=\mu\_{p}, so

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐛=−𝐀​μp.\mathbf{b}=-\mathbf{A}\mu\_{p}. |  | (86) |

Substituting into the second condition and expanding:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝔼p​[𝐬p​(𝐱)​𝐱⊤]\displaystyle\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})\mathbf{x}^{\top}] | =𝐀​𝔼p​[𝐱𝐱⊤]+𝐛​𝔼p​[𝐱]⊤\displaystyle=\mathbf{A}\mathbb{E}\_{p}[\mathbf{x}\mathbf{x}^{\top}]+\mathbf{b}\mathbb{E}\_{p}[\mathbf{x}]^{\top} |  | (87) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =𝐀​𝔼p​[𝐱𝐱⊤]−𝐀​μp​μp⊤\displaystyle=\mathbf{A}\mathbb{E}\_{p}[\mathbf{x}\mathbf{x}^{\top}]-\mathbf{A}\mu\_{p}\mu\_{p}^{\top} |  | (88) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =𝐀⁡(𝔼p​[𝐱𝐱⊤]−μp​μp⊤)\displaystyle=\mathbf{A}(\mathbb{E}\_{p}[\mathbf{x}\mathbf{x}^{\top}]-\mu\_{p}\mu\_{p}^{\top}) |  | (89) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =𝐀​Σp.\displaystyle=\mathbf{A}\Sigma\_{p}. |  | (90) |

Again by Stein’s identity, 𝔼p​[𝐬p​(𝐱)​𝐱⊤]=−𝐈d\mathbb{E}\_{p}[\mathbf{s}\_{p}(\mathbf{x})\mathbf{x}^{\top}]=-\mathbf{I}\_{d}, thus

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐀=−Σp−1.\mathbf{A}=-\Sigma\_{p}^{-1}. |  | (91) |

Combining ([86](#A2.E86 "In B.2.5 Variational characterization via 𝐿^2 projection ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) and ([91](#A2.E91 "In B.2.5 Variational characterization via 𝐿^2 projection ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) recovers

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐬qp​(𝐱)=𝐀𝐱+𝐛=−Σp−1​(𝐱−μp),\mathbf{s}\_{q\_{p}}(\mathbf{x})=\mathbf{A}\mathbf{x}+\mathbf{b}=-\Sigma\_{p}^{-1}(\mathbf{x}-\mu\_{p}), |  | (92) |

which is exactly the score of the moment-matched Gaussian qp=𝒩⁡(μp,Σp)q\_{p}=\mathcal{N}(\mu\_{p},\Sigma\_{p}).

Therefore, 𝐬qp\mathbf{s}\_{q\_{p}} is the orthogonal projection of 𝐬p\mathbf{s}\_{p} onto the space of affine functions in L2​(p)L^{2}(p), and the residual 𝜼p:=𝐬p−𝐬qp\bm{\eta}\_{p}:=\mathbf{s}\_{p}-\mathbf{s}\_{q\_{p}} is orthogonal to all affine functions. This yields a Pythagorean energy decomposition:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼p​[‖𝐬p‖2]=𝔼p​[‖𝐬qp‖2]+𝔼p​[‖𝜼p‖2].\mathbb{E}\_{p}[\|\mathbf{s}\_{p}\|^{2}]=\mathbb{E}\_{p}[\|\mathbf{s}\_{q\_{p}}\|^{2}]+\mathbb{E}\_{p}[\|\bm{\eta}\_{p}\|^{2}]. |  | (93) |

##### Implications for the field decomposition.

This projection property holds within each distribution separately: 𝜼θ\bm{\eta}\_{\theta} is the L2​(pθ)L^{2}(p\_{\theta})-orthogonal residual, and 𝜼r\bm{\eta}\_{r} is the L2​(pr)L^{2}(p\_{r})-orthogonal residual. The Pythagorean decomposition ([93](#A2.E93 "In B.2.5 Variational characterization via 𝐿^2 projection ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")) applies to each score function individually under its own measure.

However, the difference field 𝐠KL=(𝐬θ−𝐬r)\mathbf{g}\_{\mathrm{KL}}=(\mathbf{s}\_{\theta}-\mathbf{s}\_{r}) does not automatically inherit this orthogonality structure. While each residual has mean zero under its own measure, the cross-terms between 𝐠KLG=(𝐬qθ−𝐬qr)\mathbf{g}\_{\mathrm{KL}}^{\mathrm{G}}=(\mathbf{s}\_{q\_{\theta}}-\mathbf{s}\_{q\_{r}}) and 𝐠KLnG=(𝜼θ−𝜼r)\mathbf{g}\_{\mathrm{KL}}^{\mathrm{nG}}=(\bm{\eta}\_{\theta}-\bm{\eta}\_{r}) need not vanish under either pθp\_{\theta} or prp\_{r}. When these cross-moments exist, neither vanishing cross-term is guaranteed:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼pθ​[𝐠KLG⋅𝐠KLnG]​may be nonzero,𝔼pr​[𝐠KLG⋅𝐠KLnG]​may be nonzero.\mathbb{E}\_{p\_{\theta}}[\mathbf{g}\_{\mathrm{KL}}^{\mathrm{G}}\cdot\mathbf{g}\_{\mathrm{KL}}^{\mathrm{nG}}]\;\text{may be nonzero},\quad\mathbb{E}\_{p\_{r}}[\mathbf{g}\_{\mathrm{KL}}^{\mathrm{G}}\cdot\mathbf{g}\_{\mathrm{KL}}^{\mathrm{nG}}]\;\text{may be nonzero}. |  | (94) |

The decomposition is exact algebraically but not energetically orthogonal in the combined field. The two losses therefore constrain complementary *statistical structures* rather than forming an exact orthogonal decomposition of gradient variance.

### B.3 Score–Velocity Identity

This section proves the general score–velocity identity in Eq. [1](#S2.E1 "In Score–Velocity Identity. ‣ 2 Background ‣ Intrinsic Distribution Matching") for the linear Gaussian path.
The identity is a specialization of the Gaussian-path score–velocity conversion arising in stochastic-interpolant formulations and summarized pedagogically by Holderrieth and Erives ([Holderrieth and Erives, 2025](#bib.bib71)) to the case αt=1−t,βt=t\alpha\_{t}=1{-}t,\;\beta\_{t}=t.

###### Proposition B.13 (Score–Velocity Identity for the Linear Gaussian Path) .

Let 𝐱∼p\mathbf{x}\sim p have finite second moment, let ϵ∼pz=𝒩⁡(𝟎,𝐈d)\bm{\epsilon}\sim p\_{z}=\mathcal{N}(\mathbf{0},\mathbf{I}\_{d}) be independent, and define 𝐱t=(1−t)​𝐱+t​ϵ\mathbf{x}\_{t}=(1{-}t)\mathbf{x}+t\bm{\epsilon} for t∈(0,1)t\in(0,1).
Let ptp\_{t} denote the marginal density of 𝐱t\mathbf{x}\_{t} and let 𝐬t​(𝐱t):=∇𝐱t​log​pt​(𝐱t)\mathbf{s}\_{t}(\mathbf{x}\_{t}):=\nabla\_{\mathbf{x}\_{t}}\log p\_{t}(\mathbf{x}\_{t}).
For fixed tt, the marginal velocity field is the L2​(pt)L^{2}(p\_{t})-unique minimizer, up to ptp\_{t}-null sets, over measurable vector fields:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐯t∗∈arg​min𝐯:ℝd→ℝd𝔼[∥𝐯(𝐱t)−(ϵ−𝐱)∥22],𝐯t∗(𝐱t)=𝔼[ϵ−𝐱∣𝐱t].\mathbf{v}\_{t}^{\*}\in\argmin\_{\mathbf{v}:\mathbb{R}^{d}\to\mathbb{R}^{d}}\mathbb{E}\!\left[\|\mathbf{v}(\mathbf{x}\_{t})-(\bm{\epsilon}-\mathbf{x})\|\_{2}^{2}\right],\qquad\mathbf{v}\_{t}^{\*}(\mathbf{x}\_{t})=\mathbb{E}[\bm{\epsilon}-\mathbf{x}\mid\mathbf{x}\_{t}]. |  | (95) |

Then, we have the following identity:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐬t​(𝐱t)=−𝐱t+(1−t)​𝐯t∗​(𝐱t)t.\mathbf{s}\_{t}(\mathbf{x}\_{t})=-\frac{\mathbf{x}\_{t}+(1{-}t)\mathbf{v}\_{t}^{\*}(\mathbf{x}\_{t})}{t}. |  | (96) |

###### Proof B.14 .

Step 1: Rewrite as an additive Gaussian observation model.
The OT interpolant is 𝐱t=(1−t)​𝐱+t​ϵ\mathbf{x}\_{t}=(1{-}t)\mathbf{x}+t\bm{\epsilon}. Define 𝐱′:=(1−t)​𝐱\mathbf{x}^{\prime}:=(1{-}t)\mathbf{x}. Then 𝐱t=𝐱′+t​ϵ\mathbf{x}\_{t}=\mathbf{x}^{\prime}+t\bm{\epsilon} and 𝐱t|𝐱′∼𝒩⁡(𝐱′,t2​𝐈d)\mathbf{x}\_{t}\mid\mathbf{x}^{\prime}\sim\mathcal{N}(\mathbf{x}^{\prime},t^{2}\mathbf{I}\_{d}).

Step 2: Apply the Gaussian posterior-mean identity.
For a Gaussian perturbation model 𝐲=𝐱′+σ​ϵ\mathbf{y}=\mathbf{x}^{\prime}+\sigma\bm{\epsilon}, direct differentiation of the Gaussian convolution gives 𝔼⁡[𝐱′∣𝐲]=𝐲+σ2​∇𝐲​log⁡pY​(𝐲)\mathbb{E}[\mathbf{x}^{\prime}\mid\mathbf{y}]=\mathbf{y}+\sigma^{2}\nabla\_{\mathbf{y}}\log p\_{Y}(\mathbf{y}), where pYp\_{Y} is the observation density.
In our case, 𝐲=𝐱t\mathbf{y}=\mathbf{x}\_{t}, σ=t\sigma=t, so:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼⁡[𝐱′∣𝐱t]=𝐱t+t2​𝐬t​(𝐱t).\mathbb{E}[\mathbf{x}^{\prime}\mid\mathbf{x}\_{t}]=\mathbf{x}\_{t}+t^{2}\mathbf{s}\_{t}(\mathbf{x}\_{t})\,. |  | (97) |

Step 3: Recover 𝔼⁡[x∣xt]\mathbb{E}[\mathbf{x}\mid\mathbf{x}\_{t}].
Since 𝐱′=(1−t)​𝐱\mathbf{x}^{\prime}=(1{-}t)\mathbf{x}, we have 𝔼⁡[𝐱∣𝐱t]=𝔼⁡[𝐱′∣𝐱t]/(1−t)\mathbb{E}[\mathbf{x}\mid\mathbf{x}\_{t}]=\mathbb{E}[\mathbf{x}^{\prime}\mid\mathbf{x}\_{t}]/(1{-}t):

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼⁡[𝐱∣𝐱t]=𝐱t+t2​𝐬t​(𝐱t)1−t.\mathbb{E}[\mathbf{x}\mid\mathbf{x}\_{t}]=\frac{\mathbf{x}\_{t}+t^{2}\mathbf{s}\_{t}(\mathbf{x}\_{t})}{1{-}t}\,. |  | (98) |

Step 4: Recover 𝔼⁡[ϵ∣xt]\mathbb{E}[\bm{\epsilon}\mid\mathbf{x}\_{t}].
From 𝐱t=t​ϵ+(1−t)​𝐱\mathbf{x}\_{t}=t\bm{\epsilon}+(1{-}t)\mathbf{x}, ϵ=(𝐱t−(1−t)​𝐱)/t\bm{\epsilon}=(\mathbf{x}\_{t}-(1{-}t)\mathbf{x})/t.
Taking conditional expectations:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼⁡[ϵ∣𝐱t]\displaystyle\mathbb{E}[\bm{\epsilon}\mid\mathbf{x}\_{t}] | =1t​[𝐱t−(1−t)​𝔼​[𝐱∣𝐱t]]\displaystyle=\frac{1}{t}\left[\mathbf{x}\_{t}-(1{-}t)\mathbb{E}[\mathbf{x}\mid\mathbf{x}\_{t}]\right] |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | =1t​[𝐱t−(1−t)⋅𝐱t+t2​𝐬t​(𝐱t)1−t]\displaystyle=\frac{1}{t}\left[\mathbf{x}\_{t}-(1{-}t)\cdot\frac{\mathbf{x}\_{t}+t^{2}\mathbf{s}\_{t}(\mathbf{x}\_{t})}{1{-}t}\right] |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | =1t​[𝐱t−𝐱t−t2​𝐬t​(𝐱t)]\displaystyle=\frac{1}{t}\left[\mathbf{x}\_{t}-\mathbf{x}\_{t}-t^{2}\mathbf{s}\_{t}(\mathbf{x}\_{t})\right] |  |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =−t​𝐬t​(𝐱t).\displaystyle=-t\,\mathbf{s}\_{t}(\mathbf{x}\_{t})\,. |  | (99) |

Step 5: Form the marginal velocity field.
This field is the conditional expectation of the target ϵ−𝐱\bm{\epsilon}-\mathbf{x}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐯t∗​(𝐱t)\displaystyle\mathbf{v}\_{t}^{\*}(\mathbf{x}\_{t}) | =𝔼⁡[ϵ−𝐱∣𝐱t]=𝔼⁡[ϵ∣𝐱t]−𝔼⁡[𝐱∣𝐱t]\displaystyle=\mathbb{E}[\bm{\epsilon}-\mathbf{x}\mid\mathbf{x}\_{t}]=\mathbb{E}[\bm{\epsilon}\mid\mathbf{x}\_{t}]-\mathbb{E}[\mathbf{x}\mid\mathbf{x}\_{t}] |  |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =−t​𝐬t​(𝐱t)−𝐱t+t2​𝐬t​(𝐱t)1−t.\displaystyle=-t\,\mathbf{s}\_{t}(\mathbf{x}\_{t})-\frac{\mathbf{x}\_{t}+t^{2}\mathbf{s}\_{t}(\mathbf{x}\_{t})}{1{-}t}\,. |  | (100) |

Step 6: Rearrange to obtain the identity.
Multiplying both sides by (1−t)(1{-}t):

|  |  |  |  |
| --- | --- | --- | --- |
|  | (1−t)​𝐯t∗​(𝐱t)\displaystyle(1{-}t)\mathbf{v}\_{t}^{\*}(\mathbf{x}\_{t}) | =−t⁡(1−t)​𝐬t​(𝐱t)−𝐱t−t2​𝐬t​(𝐱t)\displaystyle=-t(1{-}t)\mathbf{s}\_{t}(\mathbf{x}\_{t})-\mathbf{x}\_{t}-t^{2}\mathbf{s}\_{t}(\mathbf{x}\_{t}) |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | =−t​𝐬t​(𝐱t)​[(1−t)+t]⏟=1−𝐱t\displaystyle=-t\mathbf{s}\_{t}(\mathbf{x}\_{t})\underbrace{[(1{-}t)+t]}\_{=1}-\mathbf{x}\_{t} |  |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =−t​𝐬t​(𝐱t)−𝐱t.\displaystyle=-t\mathbf{s}\_{t}(\mathbf{x}\_{t})-\mathbf{x}\_{t}\,. |  | (101) |

Rearranging and dividing by −t-t gives

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐬t​(𝐱t)=−𝐱t+(1−t)​𝐯t∗​(𝐱t)t.\mathbf{s}\_{t}(\mathbf{x}\_{t})=-\frac{\mathbf{x}\_{t}+(1{-}t)\mathbf{v}\_{t}^{\*}(\mathbf{x}\_{t})}{t}\,. |  | (102) |

###### Remark B.15 (Boundary t=1t=1) .

At t=1t=1, 𝐱1=ϵ∼𝒩⁡(𝟎,𝐈d)\mathbf{x}\_{1}=\bm{\epsilon}\sim\mathcal{N}(\mathbf{0},\mathbf{I}\_{d}) irrespective of the clean distribution pp, so p1=pzp\_{1}=p\_{z} and 𝐬1​(𝐱1)=−𝐱1\mathbf{s}\_{1}(\mathbf{x}\_{1})=-\mathbf{x}\_{1}. The right-hand side gives −(𝐱1+0⋅𝐯1∗(𝐱1))/1=−𝐱1-(\mathbf{x}\_{1}+0\cdot\mathbf{v}\_{1}^{\*}(\mathbf{x}\_{1}))/1=-\mathbf{x}\_{1}, confirming the identity at t=1t=1.

###### Corollary B.16 (Marginal Velocity Difference Recovers Score Difference) .

For i∈{1,2}i\in\{1,2\}, let 𝐱(i)∼pi\mathbf{x}^{(i)}\sim p\_{i} have finite second moment, and independent ϵ(i)∼pz\bm{\epsilon}^{(i)}\sim p\_{z}, and define 𝐱t(i)=(1−t)​𝐱(i)+t​ϵ(i)\mathbf{x}\_{t}^{(i)}=(1{-}t)\mathbf{x}^{(i)}+t\bm{\epsilon}^{(i)} for t∈(0,1)t\in(0,1).
Let pi,tp\_{i,t} be the marginal density of 𝐱t(i)\mathbf{x}\_{t}^{(i)}, and 𝐬i,t​(𝐱t):=∇𝐱t​log​pi,t​(𝐱t)\mathbf{s}\_{i,t}(\mathbf{x}\_{t}):=\nabla\_{\mathbf{x}\_{t}}\log p\_{i,t}(\mathbf{x}\_{t})
be its marginal score. Define the corresponding marginal
velocity field by 𝐯i,t∗​(𝐱t):=𝔼⁡[ϵ(i)−𝐱(i)∣𝐱t(i)=𝐱t]\mathbf{v}\_{i,t}^{\*}(\mathbf{x}\_{t}):=\mathbb{E}[\bm{\epsilon}^{(i)}-\mathbf{x}^{(i)}\mid\mathbf{x}\_{t}^{(i)}=\mathbf{x}\_{t}].
Then, for every 𝐱t\mathbf{x}\_{t} where both quantities are well defined,

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐯1,t∗​(𝐱t)−𝐯2,t∗​(𝐱t)=−t1−t​(𝐬1,t​(𝐱t)−𝐬2,t​(𝐱t)).\mathbf{v}\_{1,t}^{\*}(\mathbf{x}\_{t})-\mathbf{v}\_{2,t}^{\*}(\mathbf{x}\_{t})=-\frac{t}{1-t}\left(\mathbf{s}\_{1,t}(\mathbf{x}\_{t})-\mathbf{s}\_{2,t}(\mathbf{x}\_{t})\right). |  | (103) |

###### Proof B.17 .

Applying the Score–Velocity Identity to each field separately:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝐬1,t​(𝐱t)\displaystyle\mathbf{s}\_{1,t}(\mathbf{x}\_{t}) | =−𝐱t+(1−t)​𝐯1,t∗​(𝐱t)t,\displaystyle=-\frac{\mathbf{x}\_{t}+(1{-}t)\mathbf{v}^{\*}\_{1,t}(\mathbf{x}\_{t})}{t}\,, |  | (104) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝐬2,t​(𝐱t)\displaystyle\mathbf{s}\_{2,t}(\mathbf{x}\_{t}) | =−𝐱t+(1−t)​𝐯2,t∗​(𝐱t)t.\displaystyle=-\frac{\mathbf{x}\_{t}+(1{-}t)\mathbf{v}^{\*}\_{2,t}(\mathbf{x}\_{t})}{t}\,. |  | (105) |

Subtracting the second from the first:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐬1,t​(𝐱t)−𝐬2,t​(𝐱t)\displaystyle\mathbf{s}\_{1,t}(\mathbf{x}\_{t})-\mathbf{s}\_{2,t}(\mathbf{x}\_{t}) | =−1t​[(𝐱t+(1−t)​𝐯1,t∗)−(𝐱t+(1−t)​𝐯2,t∗)]\displaystyle=-\frac{1}{t}\left[(\mathbf{x}\_{t}+(1{-}t)\mathbf{v}^{\*}\_{1,t})-(\mathbf{x}\_{t}+(1{-}t)\mathbf{v}^{\*}\_{2,t})\right] |  |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =−1−tt​[𝐯1,t∗​(𝐱t)−𝐯2,t∗​(𝐱t)].\displaystyle=-\frac{1{-}t}{t}\left[\mathbf{v}^{\*}\_{1,t}(\mathbf{x}\_{t})-\mathbf{v}^{\*}\_{2,t}(\mathbf{x}\_{t})\right]\,. |  | (106) |

Rearranging for the velocity difference:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐯1,t∗​(𝐱t)−𝐯2,t∗​(𝐱t)=−t1−t​(𝐬1,t​(𝐱t)−𝐬2,t​(𝐱t)).\mathbf{v}^{\*}\_{1,t}(\mathbf{x}\_{t})-\mathbf{v}^{\*}\_{2,t}(\mathbf{x}\_{t})=-\frac{t}{1{-}t}\left(\mathbf{s}\_{1,t}(\mathbf{x}\_{t})-\mathbf{s}\_{2,t}(\mathbf{x}\_{t})\right)\,. |  | (107) |

### B.4 DMD Loss: Score-Difference Identity and Regression

Following the conventions above, 𝐠KL,t​(𝐱t):=𝐬θ,t​(𝐱t)−𝐬r,t​(𝐱t)\mathbf{g}\_{\mathrm{KL},t}(\mathbf{x}\_{t}):=\mathbf{s}\_{\theta,t}(\mathbf{x}\_{t})-\mathbf{s}\_{r,t}(\mathbf{x}\_{t}) denotes the reverse-KL field of the noisy marginals pθ,tp\_{\theta,t} and pr,tp\_{r,t} at noise level tt, the time-tt analog of the endpoint field 𝐠KL=𝐬θ−𝐬r\mathbf{g}\_{\mathrm{KL}}=\mathbf{s}\_{\theta}-\mathbf{s}\_{r}.

###### Proposition B.18 (Noisy-Marginal Score Difference) .

Let 𝐯θ,t∗\mathbf{v}^{\*}\_{\theta,t} and 𝐯r,t∗\mathbf{v}^{\*}\_{r,t} denote the marginal velocity fields of pθ,tp\_{\theta,t} and pr,tp\_{r,t}, evaluated at the same 𝐱t\mathbf{x}\_{t}. Then the exact velocity difference

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐝t∗​(𝐱t):=𝐯θ,t∗​(𝐱t)−𝐯r,t∗​(𝐱t)\mathbf{d}\_{t}^{\*}(\mathbf{x}\_{t}):=\mathbf{v}^{\*}\_{\theta,t}(\mathbf{x}\_{t})-\mathbf{v}^{\*}\_{r,t}(\mathbf{x}\_{t}) |  | (108) |

is proportional to the noisy-marginal reverse-KL field:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐝t∗​(𝐱t)=t1−t​(𝐬r,t​(𝐱t)−𝐬θ,t​(𝐱t))=−t1−t​𝐠KL,t​(𝐱t),\mathbf{d}\_{t}^{\*}(\mathbf{x}\_{t})=\frac{t}{1-t}\left(\mathbf{s}\_{r,t}(\mathbf{x}\_{t})-\mathbf{s}\_{\theta,t}(\mathbf{x}\_{t})\right)=-\frac{t}{1-t}\,\mathbf{g}\_{\mathrm{KL},t}(\mathbf{x}\_{t}), |  | (109) |

where 𝐠KL,t:=𝐬θ,t−𝐬r,t\mathbf{g}\_{\mathrm{KL},t}:=\mathbf{s}\_{\theta,t}-\mathbf{s}\_{r,t}.
Equivalently, the noisy-marginal distribution gradient can be recovered as

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐠KL,t​(𝐱t)=−1−tt​𝐝t∗​(𝐱t).\mathbf{g}\_{\mathrm{KL},t}(\mathbf{x}\_{t})=-\frac{1-t}{t}\mathbf{d}\_{t}^{\*}(\mathbf{x}\_{t}). |  | (110) |

###### Proof B.19 .

By with indices 1=θ1=\theta and 2=r2=r,

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝐝t∗\displaystyle\mathbf{d}\_{t}^{\*} | =𝐯θ,t∗−𝐯r,t∗=−t1−t​(𝐬θ,t​(𝐱t)−𝐬r,t​(𝐱t))=t1−t​(𝐬r,t​(𝐱t)−𝐬θ,t​(𝐱t)).\displaystyle=\mathbf{v}^{\*}\_{\theta,t}-\mathbf{v}^{\*}\_{r,t}=-\frac{t}{1-t}(\mathbf{s}\_{\theta,t}(\mathbf{x}\_{t})-\mathbf{s}\_{r,t}(\mathbf{x}\_{t}))=\frac{t}{1-t}(\mathbf{s}\_{r,t}(\mathbf{x}\_{t})-\mathbf{s}\_{\theta,t}(\mathbf{x}\_{t}))\,. |  | (111) |

Since 𝐠KL,t=𝐬θ,t−𝐬r,t\mathbf{g}\_{\mathrm{KL},t}=\mathbf{s}\_{\theta,t}-\mathbf{s}\_{r,t}, we have
𝐝t∗=−t1−t​𝐠KL,t​(𝐱t)\mathbf{d}\_{t}^{\*}=-\frac{t}{1-t}\,\mathbf{g}\_{\mathrm{KL},t}(\mathbf{x}\_{t}).
Rearranging gives ([110](#A2.E110 "In Proposition B.18 (Noisy-Marginal Score Difference) . ‣ B.4 DMD Loss: Score-Difference Identity and Regression ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching")).

[Prop. B.18](#A2.Thmtheorem18 "Proposition B.18 (Noisy-Marginal Score Difference) . ‣ B.4 DMD Loss: Score-Difference Identity and Regression ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching") is exact for marginal velocity fields and time-tt noisy marginals only when both fields recover their respective exact marginals at the same (𝐱t,t)(\mathbf{x}\_{t},t).
Practical neural branches and mixed objectives do not guarantee recovery of these exact marginal velocities.
TwinFlow and APEX use internally separated branches to turn this conversion into practical one-step distribution estimators ([Cheng et al., 2025](#bib.bib56); [Liu et al., 2026a](#bib.bib61)); we adopt APEX-style condition separation with 𝐜fake=−𝐜\mathbf{c}\_{\mathrm{fake}}=-\mathbf{c} and use the losses defined in [Section 4.1](#S4.SS1 "4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching").
In practice, 𝐝^t​(𝐱t∣𝐜):=𝐯^θ,t​(𝐱t∣𝐜)−𝐯^r,t​(𝐱t∣𝐜)\widehat{\mathbf{d}}\_{t}(\mathbf{x}\_{t}\mid\mathbf{c}):=\widehat{\mathbf{v}}\_{\theta,t}(\mathbf{x}\_{t}\mid\mathbf{c})-\widehat{\mathbf{v}}\_{r,t}(\mathbf{x}\_{t}\mid\mathbf{c}) approximates 𝐝t∗​(𝐱t)\mathbf{d}\_{t}^{\*}(\mathbf{x}\_{t}). The correction queries it at 𝐱^0,t′sg\widehat{\mathbf{x}}\_{0,t^{\prime}}^{\mathop{\operatorname{sg}}\nolimits} and detaches the result after weighting and normalization. With neither processing step, 𝐝^t′DMD=sg(𝐝^t′​(𝐱^0,t′sg∣𝐜))\widehat{\mathbf{d}}\_{t^{\prime}}^{\mathrm{DMD}}=\mathop{\operatorname{sg}}\nolimits\!\left(\widehat{\mathbf{d}}\_{t^{\prime}}(\widehat{\mathbf{x}}\_{0,t^{\prime}}^{\mathop{\operatorname{sg}}\nolimits}\mid\mathbf{c})\right). In Eq. [11](#S4.E11 "In Velocity and endpoint regression. ‣ 4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching"), subtracting 𝐝^t′DMD\widehat{\mathbf{d}}\_{t^{\prime}}^{\mathrm{DMD}} from the velocity target adds t​𝐝^t′DMDt\widehat{\mathbf{d}}\_{t^{\prime}}^{\mathrm{DMD}} to the endpoint target.

##### Gradient of the detached DMD regression.

For fixed 𝐱t\mathbf{x}\_{t} and t>0t>0, both targets in Eq. [11](#S4.E11 "In Velocity and endpoint regression. ‣ 4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching") are held constant during differentiation. Their velocity-to-endpoint conversion gives

|  |  |  |
| --- | --- | --- |
|  | 𝐱^0−𝐱0DMD=−t⁡(𝑭θ​(𝐱t,t,𝐜)−𝐯tDMD),ℓx​(t)=t2​ℓv​(t).\widehat{\mathbf{x}}\_{0}-\mathbf{x}\_{0}^{\mathrm{DMD}}=-t\bigl(\bm{F}\_{\theta}(\mathbf{x}\_{t},t,\mathbf{c})-\mathbf{v}\_{t}^{\mathrm{DMD}}\bigr),\qquad\ell\_{x}(t)=t^{2}\ell\_{v}(t). |  |

Hence ∇θℓx​(t)=t2​∇θℓv​(t)\nabla\_{\theta}\ell\_{x}(t)=t^{2}\nabla\_{\theta}\ell\_{v}(t), and the equal-weight DMD loss in Eq. [12](#S4.E12 "In Velocity and endpoint regression. ‣ 4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching") satisfies

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒscore\displaystyle\mathcal{L}\_{\text{score}} | =𝔼⁡[(1+t2)​ℓv​(t)],\displaystyle=\mathbb{E}\!\left[(1+t^{2})\ell\_{v}(t)\right], |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇θℒscore\displaystyle\nabla\_{\theta}\mathcal{L}\_{\text{score}} | =2​𝔼​[(1+t2)​[Jθ​𝑭θ​(𝐱t,t,𝐜)]⊤​𝐝^t′DMD].\displaystyle=2\mathbb{E}\!\left[(1+t^{2})[J\_{\theta}\bm{F}\_{\theta}(\mathbf{x}\_{t},t,\mathbf{c})]^{\top}\widehat{\mathbf{d}}\_{t^{\prime}}^{\mathrm{DMD}}\right]. |  |

If the correction equals the exact, unweighted velocity difference 𝐝t′∗​(𝐱^0,t′sg)\mathbf{d}\_{t^{\prime}}^{\*}(\widehat{\mathbf{x}}\_{0,t^{\prime}}^{\mathop{\operatorname{sg}}\nolimits}), then Eq. [109](#A2.E109 "In Proposition B.18 (Noisy-Marginal Score Difference) . ‣ B.4 DMD Loss: Score-Difference Identity and Regression ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching") and Jθ​𝐱^0=−t​Jθ​𝑭θJ\_{\theta}\widehat{\mathbf{x}}\_{0}=-tJ\_{\theta}\bm{F}\_{\theta} yield the per-example identity

|  |  |  |
| --- | --- | --- |
|  | ∇θ(ℓv​(t)+ℓx​(t))=2​t′​(1+t2)t⁡(1−t′)​[Jθ​𝐱^0]⊤​𝐠KL,t′​(𝐱^0,t′sg).\nabla\_{\theta}(\ell\_{v}(t)+\ell\_{x}(t))=\frac{2t^{\prime}(1+t^{2})}{t(1-t^{\prime})}[J\_{\theta}\widehat{\mathbf{x}}\_{0}]^{\top}\mathbf{g}\_{\mathrm{KL},t^{\prime}}(\widehat{\mathbf{x}}\_{0,t^{\prime}}^{\mathop{\operatorname{sg}}\nolimits}). |  |

This is a pointwise pullback of the field defined by pθ,t′p\_{\theta,t^{\prime}} and pr,t′p\_{r,t^{\prime}}. An on-policy KL interpretation additionally requires the queried prediction law to agree with the model law used to train the model-velocity branch. For the one-step law of [Section 3.1](#S3.SS1 "3.1 Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching"), this agreement is immediate at t=1t=1, 𝐱t=𝐳\mathbf{x}\_{t}=\mathbf{z}, but is not implied for intermediate regression inputs.
For the squared losses above, the two per-example gradients are collinear and their combination changes the time weighting and magnitude; at t=1t=1, ℓx=ℓv\ell\_{x}=\ell\_{v}. Separate residual-dependent normalizations can change the proportionality factor and must be included when applying this calculation to a normalized loss.
With approximate branches and correction processing, Eq. [12](#S4.E12 "In Velocity and endpoint regression. ‣ 4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching") does not in general have the same gradient as the unweighted time-averaged noisy reverse KL.

### B.5 Internal model-velocity training

Draw 𝐳,ϵ∼pz\mathbf{z},\bm{\epsilon}\sim p\_{z} independently, set 𝐱θsg:=sg(Gθ​(𝐳,𝐜))\mathbf{x}\_{\theta}^{\mathop{\operatorname{sg}}\nolimits}:=\mathop{\operatorname{sg}}\nolimits(G\_{\theta}(\mathbf{z},\mathbf{c})) and 𝐱θ,tsg:=(1−t)​𝐱θsg+t​ϵ\mathbf{x}\_{\theta,t}^{\mathop{\operatorname{sg}}\nolimits}:=(1{-}t)\mathbf{x}\_{\theta}^{\mathop{\operatorname{sg}}\nolimits}+t\bm{\epsilon}, and minimize

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒfake​(θ)=𝔼𝐳,ϵ,t,𝐜​[‖𝐯^θ,t​(𝐱θ,tsg∣𝐜)−(ϵ−𝐱θsg)‖22],\mathcal{L}\_{\text{fake}}(\theta)={\mathbb{E}}\_{\mathbf{z},\bm{\epsilon},t,\mathbf{c}}\left[\|\widehat{\mathbf{v}}\_{\theta,t}(\mathbf{x}\_{\theta,t}^{\mathop{\operatorname{sg}}\nolimits}\mid\mathbf{c})-(\bm{\epsilon}-\mathbf{x}\_{\theta}^{\mathop{\operatorname{sg}}\nolimits})\|\_{2}^{2}\right]\,, |  | (112) |

Here 𝐜∼pc\mathbf{c}\sim p\_{c}, 𝐳,ϵ∼pz\mathbf{z},\bm{\epsilon}\sim p\_{z} are independent, and tt is independently sampled from a distribution supported on (0,1)(0,1). This auxiliary regression uses the one-step output law pθp\_{\theta} defined in [Section 3.1](#S3.SS1 "3.1 Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching").
Gradients pass through the model-velocity branch, while generated samples and regression targets are detached. The branches share θ\theta, so this auxiliary regression also updates shared parameters.

### B.6 Gradient of the Feature-Moment Loss

##### Fixed-feature updates.

Within an update, the EMA feature-map parameters and queued features are held fixed, while derivatives through the current model samples are retained.
The feature-moment loss therefore cannot be reduced by directly changing the feature-map parameters within that update.
This removes a direct feature-collapse shortcut of one update but does not rule out slow degeneration as the EMA map evolves over training.

###### Proposition B.20 (Gradient of the Feature-Moment Loss) .

Let 𝐡n\mathbf{h}\_{n}, n=1,…,Nϕn=1,\ldots,N\_{\phi}, denote model features: current entries 𝐡n=ϕ⁡(𝐱n,𝐜n)\mathbf{h}\_{n}=\phi(\mathbf{x}\_{n},\mathbf{c}\_{n}) retain gradients, while stored queue entries are detached. Define the empirical means and biased empirical variances

|  |  |  |
| --- | --- | --- |
|  | μ^θϕ:=Nϕ−1​∑n𝐡n,ν^θ,jϕ:=Nϕ−1​∑n(hn,j−μ^θ,jϕ)2,\widehat{\mu}\_{\theta}^{\phi}:=N\_{\phi}^{-1}\sum\_{n}\mathbf{h}\_{n}\,,\qquad\widehat{\nu}\_{\theta,j}^{\phi}:=N\_{\phi}^{-1}\sum\_{n}(h\_{n,j}-\widehat{\mu}\_{\theta,j}^{\phi})^{2}\,, |  |

and for the queued reference features, let {𝐡kr}k=1K\{\mathbf{h}\_{k}^{r}\}\_{k=1}^{K} denote the KK pre-computed feature vectors stored in 𝒬r\mathcal{Q}\_{r} (computed as ϕ⁡(𝐱k,𝐜k)\phi(\mathbf{x}\_{k},\mathbf{c}\_{k}) at enqueue time and detached), and define

|  |  |  |
| --- | --- | --- |
|  | μ^rϕ:=K−1​∑k=1K𝐡kr,ν^r,jϕ:=K−1​∑k=1K(hk,jr−μ^r,jϕ)2;\widehat{\mu}\_{r}^{\phi}:=K^{-1}\!\sum\_{k=1}^{K}\!\mathbf{h}\_{k}^{r}\,,\qquad\widehat{\nu}\_{r,j}^{\phi}:=K^{-1}\!\sum\_{k=1}^{K}\!(h^{r}\_{k,j}-\widehat{\mu}\_{r,j}^{\phi})^{2}\,; |  |

assume ν^θ,jϕ>0\widehat{\nu}\_{\theta,j}^{\phi}>0. These are estimators of the population quantities μiϕ,νi,jϕ\mu\_{i}^{\phi},\nu\_{i,j}^{\phi} defined in [Section 4.2](#S4.SS2.SSS0.Px2 "Matching feature moments. ‣ 4.2 Feature-Moment Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching"). Write ℒ^pop\widehat{\mathcal{L}}\_{\text{pop}} for Eq. [13](#S4.E13 "In Matching feature moments. ‣ 4.2 Feature-Moment Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching") evaluated at these empirical moments. Its gradient with respect to a current feature 𝐡k\mathbf{h}\_{k} is

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∂ℒ^pop∂hk,j=2Nϕ​[(μ^θ,jϕ−μ^r,jϕ)+hk,j−μ^θ,jϕν^θ,jϕ​(ν^θ,jϕ−ν^r,jϕ)].\frac{\partial\widehat{\mathcal{L}}\_{\text{pop}}}{\partial h\_{k,j}}=\frac{2}{N\_{\phi}}\!\left[(\widehat{\mu}\_{\theta,j}^{\phi}-\widehat{\mu}\_{r,j}^{\phi})+\frac{h\_{k,j}-\widehat{\mu}\_{\theta,j}^{\phi}}{\sqrt{\widehat{\nu}\_{\theta,j}^{\phi}}}\left(\sqrt{\widehat{\nu}\_{\theta,j}^{\phi}}-\sqrt{\widehat{\nu}\_{r,j}^{\phi}}\right)\right]\!. |  | (113) |

This is the exact gradient of the empirical objective at fixed queues; it is not, in general, an unbiased estimate of the gradient of the population loss ℒpop\mathcal{L}\_{\text{pop}}.

###### Proof B.21 .

The empirical loss decomposes as ℒ^pop=ℒμ+ℒσ\widehat{\mathcal{L}}\_{\text{pop}}=\mathcal{L}\_{\mu}+\mathcal{L}\_{\sigma}, where

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | ℒμ\displaystyle\mathcal{L}\_{\mu} | =∑j(μ^θ,jϕ−μ^r,jϕ)2,\displaystyle=\sum\_{j}(\widehat{\mu}\_{\theta,j}^{\phi}-\widehat{\mu}\_{r,j}^{\phi})^{2}\,, |  | (114) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | ℒσ\displaystyle\mathcal{L}\_{\sigma} | =∑j(ν^θ,jϕ−ν^r,jϕ)2.\displaystyle=\sum\_{j}(\sqrt{\widehat{\nu}\_{\theta,j}^{\phi}}-\sqrt{\widehat{\nu}\_{r,j}^{\phi}})^{2}\,. |  | (115) |

(a) Mean term.
Since ∂μ^θ,jϕ/∂hk,j=1/Nϕ\partial\widehat{\mu}\_{\theta,j}^{\phi}/\partial h\_{k,j}=1/N\_{\phi},

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∂ℒμ∂hk,j=2Nϕ​(μ^θ,jϕ−μ^r,jϕ).\frac{\partial\mathcal{L}\_{\mu}}{\partial h\_{k,j}}=\frac{2}{N\_{\phi}}(\widehat{\mu}\_{\theta,j}^{\phi}-\widehat{\mu}\_{r,j}^{\phi})\,. |  | (116) |

(b) Variance term.
Since ν^θ,jϕ=Nϕ−1​∑n(hn,j−μ^θ,jϕ)2\widehat{\nu}\_{\theta,j}^{\phi}=N\_{\phi}^{-1}\sum\_{n}(h\_{n,j}-\widehat{\mu}\_{\theta,j}^{\phi})^{2},

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∂(hn,j−μ^θ,jϕ)∂hk,j=δn​k−1Nϕ.\frac{\partial(h\_{n,j}-\widehat{\mu}\_{\theta,j}^{\phi})}{\partial h\_{k,j}}=\delta\_{nk}-\frac{1}{N\_{\phi}}\,. |  | (117) |

By the chain rule and the centered-sum identity, summing over nn gives

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∂ν^θ,jϕ∂hk,j=2Nϕ​(hk,j−μ^θ,jϕ).\displaystyle\frac{\partial\widehat{\nu}\_{\theta,j}^{\phi}}{\partial h\_{k,j}}=\frac{2}{N\_{\phi}}(h\_{k,j}-\widehat{\mu}\_{\theta,j}^{\phi})\,. |  | (118) |

Applying the chain rule to the standard deviation gives

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∂ℒσ∂hk,j=2Nϕ​hk,j−μ^θ,jϕν^θ,jϕ​(ν^θ,jϕ−ν^r,jϕ).\displaystyle\frac{\partial\mathcal{L}\_{\sigma}}{\partial h\_{k,j}}=\frac{2}{N\_{\phi}}\frac{h\_{k,j}-\widehat{\mu}\_{\theta,j}^{\phi}}{\sqrt{\widehat{\nu}\_{\theta,j}^{\phi}}}(\sqrt{\widehat{\nu}\_{\theta,j}^{\phi}}-\sqrt{\widehat{\nu}\_{r,j}^{\phi}})\,. |  | (119) |

Combining.
Summing (a) and (b):

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∂ℒ^pop∂hk,j=2Nϕ​[(μ^θ,jϕ−μ^r,jϕ)+hk,j−μ^θ,jϕν^θ,jϕ​(ν^θ,jϕ−ν^r,jϕ)].\frac{\partial\widehat{\mathcal{L}}\_{\text{pop}}}{\partial h\_{k,j}}=\frac{2}{N\_{\phi}}\left[(\widehat{\mu}\_{\theta,j}^{\phi}-\widehat{\mu}\_{r,j}^{\phi})+\frac{h\_{k,j}-\widehat{\mu}\_{\theta,j}^{\phi}}{\sqrt{\widehat{\nu}\_{\theta,j}^{\phi}}}\left(\sqrt{\widehat{\nu}\_{\theta,j}^{\phi}}-\sqrt{\widehat{\nu}\_{r,j}^{\phi}}\right)\right]\!. |  | (120) |

For a stabilized version with ν^i,jϕ+δ\sqrt{\widehat{\nu}\_{i,j}^{\phi}+\delta}, where δ>0\delta>0 is a scalar stabilizer, the same derivation replaces every standard deviation in the gradient by its stabilized value, including the denominator. The displayed gradient is for the unstabilized objective under the stated positive-variance assumption.

### B.7 Covariance Contraction Under Regression

This result shows a limitation of interpreting squared-error regression as distribution matching: a conditional-mean predictor need not preserve the target covariance. It is a separate observation about regression, not a consequence of the reverse-KL field decomposition or a claim that DMD lacks variance information.

###### Proposition B.22 (Covariance Contraction Under Regression) .

Let (𝐗,𝐘)(\mathbf{X},\mathbf{Y}) be any square-integrable jointly distributed random vectors and let 𝐦⁡(𝐘):=𝔼⁡[𝐗∣𝐘]\mathbf{m}(\mathbf{Y}):=\mathbb{E}[\mathbf{X}\mid\mathbf{Y}] be the optimal squared-error predictor. Then

|  |  |  |  |
| --- | --- | --- | --- |
|  | Cov⁡(𝐦⁡(𝐘))⪯Cov⁡(𝐗).\operatorname{Cov}(\mathbf{m}(\mathbf{Y}))\preceq\operatorname{Cov}(\mathbf{X}). |  | (121) |

Moreover, Tr⁡Cov⁡(𝐦⁡(𝐘))<Tr⁡Cov⁡(𝐗)\operatorname{Tr}\operatorname{Cov}(\mathbf{m}(\mathbf{Y}))<\operatorname{Tr}\operatorname{Cov}(\mathbf{X}) whenever 𝔼⁡[Tr⁡Cov⁡(𝐗∣𝐘)]>0\mathbb{E}[\operatorname{Tr}\operatorname{Cov}(\mathbf{X}\mid\mathbf{Y})]>0.

###### Proof B.23 .

By the law of total covariance,

|  |  |  |  |
| --- | --- | --- | --- |
|  | Cov⁡(𝐗)=𝔼⁡[Cov⁡(𝐗∣𝐘)]+Cov⁡(𝔼⁡[𝐗∣𝐘])=𝔼⁡[Cov⁡(𝐗∣𝐘)]+Cov⁡(𝐦⁡(𝐘)).\operatorname{Cov}(\mathbf{X})=\mathbb{E}[\operatorname{Cov}(\mathbf{X}\mid\mathbf{Y})]+\operatorname{Cov}(\mathbb{E}[\mathbf{X}\mid\mathbf{Y}])=\mathbb{E}[\operatorname{Cov}(\mathbf{X}\mid\mathbf{Y})]+\operatorname{Cov}(\mathbf{m}(\mathbf{Y})). |  | (122) |

The conditional-covariance term is positive semidefinite, proving the matrix inequality. Taking traces gives the strict statement.

This proposition applies only when the trained predictor realizes the conditional mean under the chosen squared-error coupling.
Strict covariance contraction occurs only when unresolved conditional variance remains.
It therefore motivates possible variance suppression in ambiguous endpoint regression, but it does not imply that deterministic or one-step generators generally underestimate variance.
Note that exact score differences *do* contain variance information: for pθ=𝒩⁡(0,σθ2)p\_{\theta}=\mathcal{N}(0,\sigma\_{\theta}^{2}) and pr=𝒩⁡(0,σr2)p\_{r}=\mathcal{N}(0,\sigma\_{r}^{2}),

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐬θ​(x)−𝐬r​(x)=−xσθ2+xσr2,\mathbf{s}\_{\theta}(x)-\mathbf{s}\_{r}(x)=-\frac{x}{\sigma\_{\theta}^{2}}+\frac{x}{\sigma\_{r}^{2}}\,, |  | (123) |

so the descent direction 𝐬r​(x)−𝐬θ​(x)=x⁡(1/σθ2−1/σr2)\mathbf{s}\_{r}(x)-\mathbf{s}\_{\theta}(x)=x(1/\sigma\_{\theta}^{2}-1/\sigma\_{r}^{2}) pushes samples outward when σθ<σr\sigma\_{\theta}<\sigma\_{r}.
The learned pointwise estimator can nevertheless be noisy because it depends on the accuracy of the learned velocity branches and random time/noise samples.
The pooled feature-moment loss provides an explicit population-statistic correction.
Under an approximately independent, stationary-feature idealization with finite moments, the model- and reference-side mean-estimation variances scale as O⁡(1/Nϕ)O(1/N\_{\phi}) and O⁡(1/K)O(1/K); this does not establish that its empirical parameter-gradient variance is lower than that of the DMD loss, and queue staleness can introduce bias.
