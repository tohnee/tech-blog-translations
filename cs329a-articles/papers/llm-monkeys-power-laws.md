---
title: "How Do Large Language Monkeys Get Their Power (Laws)?"
arxiv: 2502.17578
source: https://arxiv.org/abs/2502.17578
crawled: 2026-09-23
---

marginparsep has been altered.
  
topmargin has been altered.
  
marginparpush has been altered.

The page layout violates the ICML style.

Please do not change the page layout, or include packages like geometry,
savetrees, or fullpage, which change it for you.

We’re not able to reliably undo arbitrary changes to the style. Please remove
the offending package(s), or layout-changing commands and try again.

 

How Do Large Language Monkeys Get Their Power (Laws)?

 

Rylan Schaeffer 1
Joshua Kazdan 2
John Hughes 34
Jordan Juravsky 1
Sara Price 4
Aengus Lynch 45
Erik Jones 6
Robert Kirk 5
Azalia Mirhoseini 1
Sanmi Koyejo 1

###### Abstract

Recent research across mathematical problem solving, proof assistant programming and multimodal jailbreaking documents a striking finding: when (multimodal) language model tackle a suite of tasks with multiple attempts per task – succeeding if any attempt is correct – then the negative log of the average success rate scales a power law in the number of attempts.
In this work, we identify an apparent puzzle: a simple mathematical calculation predicts that on each problem, the failure rate should fall exponentially with the number of attempts.
We confirm this prediction empirically, raising a question: from where does aggregate polynomial scaling emerge?
We then answer this question by demonstrating per-problem exponential scaling can be made consistent with aggregate polynomial scaling if the distribution of single-attempt success probabilities is heavy tailed such that a small fraction of tasks with extremely low success probabilities collectively warp the aggregate success trend into a power law - even as each problem scales exponentially on its own.
We further demonstrate that this distributional perspective explains previously observed deviations from power law scaling, and provides a simple method for forecasting the power law exponent with an order of magnitude lower relative error, or equivalently, ∼2−4{\sim}2-4 orders of magnitude less inference compute.
Overall, our work contributes to a better understanding of how neural language model performance improves with scaling inference compute and the development of scaling-predictable evaluations of (multimodal) language models.

## 1 Introduction

Scaling behaviors of large neural language models have surprised and fascinated engineers, scientists and society alike ([Hestness et al., 2017](#bib.bib50); [Kaplan et al., 2020](#bib.bib59); [Brown et al., 2020a](#bib.bib22); [Hoffmann et al., 2022](#bib.bib52); [Ganguli et al., 2022](#bib.bib39); [Sorscher et al., 2022](#bib.bib100); [Wei et al., 2022b](#bib.bib112); [Schaeffer et al., 2023](#bib.bib93); [OpenAI et al., 2024](#bib.bib78)), shaping engineering, economic and governmental interests in frontier AI systems ([Bommasani et al., 2021](#bib.bib16); [Eloundou et al., 2023](#bib.bib36); [Anderljung et al., 2023](#bib.bib5); [Wang et al., 2023](#bib.bib110); [Reuel et al., 2024](#bib.bib85); [Besiroglu et al., 2024a](#bib.bib12); [Maslej et al., 2024](#bib.bib68)). For a more thorough exposition of relevant literature, please see Related Work (Section [6](#S6 "6 Related Work")).

Figure 1: Power Law Scaling in Language Models from Repeat Sampling. Top: [Brown et al. (2024)](#bib.bib21) found the negative log average pass rate −log⁡(pass𝒟​@​k)-\log(\operatorname{pass_{\mathcal{D}}@k}) at solving mathematical problems scales polynomially (i.e., as a power law) with the number of independent attempts per problem kk. Bottom: [Hughes et al. (2024)](#bib.bib54) similarly found the negative log average attack success rate −log⁡(ASR𝒟​@​k)-\log(\operatorname{ASR_{\mathcal{D}}@k}) when jailbreaking multimodal language models scales polynomially with the number of jailbreak attempts per prompt. Should such power law scaling be expected?
From where do large language monkeys obtain their power (laws)?

Figure 2: Schematic: The Origin of Power Laws from Scaling Inference Compute via Repeat Sampling. The −log⁡(pass𝒟​@​k)-\log(\operatorname{pass_{\mathcal{D}}@k}) scales as a power law with the number of attempts per problem kk (left). This arises from a combination of two factors: (1) for each problem, −log⁡(passi​@​k)-\log(\operatorname{pass_{i}@k}) scales exponentially with kk (center), and (2) the distribution (over problems in the dataset) of single-attempt success rates passi​@​1\operatorname{pass_{i}@1} itself has a left power-law tail of small values (right).

One direction of renewed interest is inference-time compute scaling, whereby compute is controllably increased at inference to improve the performance of a model, e.g., [Pachocki et al. (2024)](#bib.bib80). In this direction, recent research discovered that language model success rates scale predictably with the number of independent attempts made at accomplishing a task.
Specifically, in a paper titled, “Large Language Monkeys: Scaling Inference Compute with Repeated Sampling," [Brown et al. (2024)](#bib.bib21) studied how language model performance changes at mathematical problem solving and coding problems when kk independent attempts are sampled per problem. Performance on the ii-th problem was measured using the expected (over attempts) success rate ([Kulal et al., 2019](#bib.bib62); [Chen et al., 2021](#bib.bib27)), defined as:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | passi​@​k⁡=def\displaystyle\operatorname{pass_{i}@k}\,\defeq\, |  | (1) |
|  |  | 𝔼k​ Attempts⁡[𝕀⁡[Any attempt on i-th problem succeeds]].\displaystyle\mathop{\raisebox{3.0pt}{$\mathbb{E}$}}_{\begin{subarray}{c}k\text{ Attempts}\end{subarray}}\Big[\mathbb{I}[\text{Any attempt on $i$-th problem succeeds}]\Big]. |  |

Using the unbiased and numerically stable estimator of [Chen et al. (2021)](#bib.bib27) (for details, see Appendix [B](#A2 "Appendix B Estimating Success Rates Using ( ) ’s Estimator")), [Brown et al. (2024)](#bib.bib21) found that the negative log averaged-over-PP-problems success rate falls as a power law with the number of independent attempts per problem kk:

|  |  |  |  |
| --- | --- | --- | --- |
|  | −log⁡(1P​∑i=1Ppassi​@​k)≈a​k−b,-\log\Bigg(\frac{1}{P}\sum_{i=1}^{P}\operatorname{pass_{i}@k}\Bigg)\approx ak^{-b}, |  | (2) |

for model-specific and benchmark-specific constants a,b>0a,b>0 (Fig. [1](#S1.F1 "Figure 1 ‣ 1 Introduction") Top). Soon after, on a separate topic of jailbreaking multimodal language models via text, image and audio attacks, independent work by [Hughes et al. (2024)](#bib.bib54) studied jailbreaking success rates when kk independent attempts are made per harmful prompt. Performance was measured using Attack Success Rate (ASR) at kk:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | ASRi​@​k⁡=def\displaystyle\operatorname{ASR_{i}@k}\,\defeq\, |  | (3) |
|  |  | 𝔼k​ Attempts⁡[𝕀⁡[Any attack on i-th prompt succeeds]].\displaystyle\mathop{\raisebox{3.0pt}{$\mathbb{E}$}}_{\begin{subarray}{c}k\text{ Attempts}\end{subarray}}\Big[\mathbb{I}[\text{Any attack on $i$-th prompt succeeds}]\Big]. |  |

This “Best-of-N Jailbreaking" attack similarly discovered that the negative log averaged-over-PP-prompts attack success rate fell as a power law with the number of jailbreak attempts per prompt kk:

|  |  |  |  |
| --- | --- | --- | --- |
|  | −log⁡(1P​∑i=1PASRi​@​k)≈a​k−b,-\log\Bigg(\frac{1}{P}\sum_{i=1}^{P}\operatorname{ASR_{i}@k}\Bigg)\approx ak^{-b}, |  | (4) |

for model-specific and modality-specific constants a,b>0a,b>0 (Fig. [1](#S1.F1 "Figure 1 ‣ 1 Introduction") Bottom).
For the specific coefficients from both papers, see Appendix. [C](#A3 "Appendix C Fitting Power Laws to Large Language Monkeys and Best-of-N Jailbreaking").
As a minor matter of terminology, both papers frame their results in terms of “coverage" – the fraction of problems that can be solved after kk attempts per problem – but as [Brown et al. (2024)](#bib.bib21) pointed out, coverage is equivalent to the average success rate (Appendix [D](#A4 "Appendix D Mathematical Equivalence Between Coverage and Average Success Rate")); we prefer this latter framing as it avoids the binary implication that each problem either is or is not solved after kk attempts.

## 2 Should Power Law Scaling Be Expected?

Should we expect large language monkeys to have such power (laws)? That is, should the negative log of the average success rate scale polynomially with the number of independent attempts kk? As we now explain mathematically and demonstrate empirically, such polynomial scaling with kk is perhaps surprising because, for any single problem, the negative log success rate at kk should fall exponentially with kk; the intuition is that passi​@​k\operatorname{pass_{i}@k} is 1 unless all attempts fail, and since attempts are independent, the probability that all fail is exponentially unlikely with the number of attempts.

Figure 3: Per-problem performance scales exponentially with the number of attempts per problem kk.
Top: Pythia language models on 128 problems from MATH, with performance on the ii-th problem measured as −log⁡(passi​@​k)-\log(\operatorname{pass_{i}@k}). Bottom: Frontier AI models on jailbreaking prompts from HarmBench, with performance on the ii-th problem measured as −log⁡(ASRi​@​k)-\log(\operatorname{ASR_{i}@k}). In both settings, on each problem, the negative log per-problem success rate falls exponentially with the number of independent attempts kk. However, the negative log average success rate falls as a power law with kk (black).

Mathematically, on any given attempt, the model has probability passi​@​1\operatorname{pass_{i}@1} of solving the ii-th problem.
Recalling that passi​@​k\operatorname{pass_{i}@k} is defined as 11 if any of the kk attempts succeed, 0 otherwise, by linearity of expectation and by independence of the kk attempts, we can rewrite passi​@​k\operatorname{pass_{i}@k} as:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | passi​@​k\displaystyle\operatorname{pass_{i}@k} | =𝔼k​ Attempts⁡[1−𝕀⁡[All k Attempts Fail]]\displaystyle=\mathop{\raisebox{3.0pt}{$\mathbb{E}$}}_{\begin{subarray}{c}k\text{ Attempts}\end{subarray}}\Big[1-\mathbb{I}[\text{All $k$ Attempts Fail}]\Big] |  | (5) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =1−∏j=1k𝔼1​ Attempt⁡[𝕀⁡[j-th Attempt Fails]].\displaystyle=1-\prod_{j=1}^{k}\mathop{\raisebox{3.0pt}{$\mathbb{E}$}}_{\begin{subarray}{c}1\text{ Attempt}\end{subarray}}\Big[\mathbb{I}[\text{$j$-th Attempt Fails}]\Big]. |  | (6) |

The probability that the jj-th attempt fails is one minus the probability that the jj-th attempt succeeds. Since each attempt is i.i.d. with success probability passi​@​1\operatorname{pass_{i}@1}, we find

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | passi​@​k\displaystyle\operatorname{pass_{i}@k} | =1−(1−passi​@​1)k.\displaystyle=1-(1-\operatorname{pass_{i}@1})^{k}. |  | (7) |

For large kk, (1−passi​@​1)k(1-\operatorname{pass_{i}@1})^{k} will be small. Recalling that the Taylor Series expansion of log⁡(1+x)\log(1+x) for small xx is ∑i=1∞(−1)i−1​xi/i≈x\sum_{i=1}^{\infty}(-1)^{i-1}x^{i}/i\approx x, we have:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | −log⁡(passi​@​k)\displaystyle-\log(\operatorname{pass_{i}@k}) | =−log⁡(1−(1−pass​@​1)k)\displaystyle=-\log\Big(1-(1-\operatorname{pass@1})^{k}\Big) |  | (8) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | ≈(1−passi​@​1)k.\displaystyle\approx(1-\operatorname{pass_{i}@1})^{k}. |  | (9) |

Figure 4: Single-Attempt Success Rates Distributions Possess Power Law-Like Left Tails. Pythia language models on 128 MATH problems (top) and frontier AI systems on 159 HarmBench prompts (bottom) exhibit distributions (over problems) of passi​@​1\operatorname{pass_{i}@1} and ASRi​@​1\operatorname{ASR_{i}@1} with power law-like tails that are well fit by scaled Beta-Binomial distributions (black dashed lines), which produce aggregate power law scaling. Note that Llama 3 8B Instruction Tuned (IT) does not possess a power law tail, explaining why the model did not exhibit aggregate power law scaling under Best-of-N jailbreaking (Sec. [4](#S4 "4 Lack of Distributional Structure Explains Deviations from Power Law Scaling")).

Thus, for any single problem, we should expect the negative log expected (over attempts) success rate to fall exponentially with kk, not polynomially with kk.

To confirm this claim, we plotted the scaling of model performance on each problem – measured either by −log⁡(passi​@​k)-\log(\operatorname{pass_{i}@k}) or by −log⁡(ASRi​@​k)-\log(\operatorname{ASR_{i}@k}) – against the number of independent attempts kk. We specifically used [Brown et al. (2024)](#bib.bib21)’s data of the Pythia language model family ([Biderman et al., 2023](#bib.bib14)) solving 128 mathematical problems from MATH [Hendrycks et al. (2021)](#bib.bib46) as well as [Hughes et al. (2024)](#bib.bib54)’s data from jailbreaking frontier AI systems – Claude, GPT4 ([OpenAI et al., 2024](#bib.bib78)), Gemini ([Team et al., 2024a](#bib.bib108); [Team et al., 2024b](#bib.bib109)) and Llama 3 8B Instruction Tuned (IT) ([Grattafiori et al., 2024](#bib.bib45)) – on 159 prompts from HarmBench ([Mazeika et al., 2024](#bib.bib69)).
For each individual mathematical problem and jailbreaking prompt, we found the negative log expected (over attempts) success rates fall exponentially with kk as expected (Fig. [3](#S2.F3 "Figure 3 ‣ 2 Should Power Law Scaling Be Expected?")), including on Llama 3 8B IT which does not exhibit an aggregate power law (Fig. [1](#S1.F1 "Figure 1 ‣ 1 Introduction")).

## 3 Distribution of Per-Problem Single-Attempt Success Rates Creates Power Law Scaling

How does polynomial scaling of the negative log average success rate emerge from exponential scaling of the negative log per-problem success rate?
The answer to this question must lie in the distribution 𝒟\mathcal{D} over benchmark problems of single attempt (i.e., k=1k=1) success rates because this distribution’s density p𝒟​(passi​@​1)p_{\mathcal{D}}(\operatorname{pass_{i}@1}) links the per-problem scaling behavior to the aggregate scaling behavior via the definition of the aggregate success rate pass𝒟​@​k\operatorname{pass_{\mathcal{D}}@k}:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | pass𝒟​@​k⁡=def​𝔼passi​@​1∼𝒟⁡[passi​@​k⁡(passi​@​1)]\displaystyle\operatorname{pass_{\mathcal{D}}@k}\;\defeq\;\mathop{\raisebox{3.0pt}{$\mathbb{E}$}}_{\operatorname{pass_{i}@1}\sim\mathcal{D}}\Big[\operatorname{pass_{i}@k}(\operatorname{pass_{i}@1})\Big] |  | (10) |
|  |  | =1−∫01(1−passi​@​1)k​p𝒟​(passi​@​1)​d​passi​@​1.\displaystyle=1-\int_{0}^{1}(1-\operatorname{pass_{i}@1})^{k}\,p_{\mathcal{D}}(\operatorname{pass_{i}@1})\,\operatorname{d\,pass_{i}@1}. |  |

Based on a known result that power laws can originate from an appropriately weighted sum of exponential functions (Appendix  [E.1](#A5.SS1 "E.1 Preliminaries: Power Laws from Weighted Exponential Functions ‣ Appendix E Aggregate Power Laws from a Probability Distribution over Exponential Functions")), we begin by considering simple distributions for the single-attempt success probabilities and asking which yield power law scaling between −log⁡(pass𝒟​@​k)-\log(\operatorname{pass_{\mathcal{D}}@k}) and kk, as well as what properties of the distributions set the scaling exponent. In Appendices [E.3](#A5.SS3 "E.3 Uniform Distribution: pass_i⁢@⁢1∼Uniform(𝛼,𝛽) ‣ Appendix E Aggregate Power Laws from a Probability Distribution over Exponential Functions")-[E.8](#A5.SS8 "E.8 Reciprocal Distribution: pass_i⁢@⁢1∼Reciprocal(𝑎,𝑏) ‣ Appendix E Aggregate Power Laws from a Probability Distribution over Exponential Functions"), we derive that several simple distributions yield power law scaling with different exponents whereas others do not:

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | −log⁡(CLOSE\displaystyle-\log\Big( | passUniform⁡(0,β≤1)⁡@​k\displaystyle\operatorname{pass_{\mathrm{Uniform}(0,\,\beta\leq 1)}}@k | )\displaystyle\Big) | ∝k−1.\displaystyle\propto k^{-1}. |  |
|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | −log⁡(CLOSE\displaystyle-\log\Big( | passBeta⁡(α,β)​@​k\displaystyle\operatorname{pass_{\operatorname{Beta(\alpha,\beta)}}@k} | )\displaystyle\Big) | ∝k−α.\displaystyle\propto k^{-\alpha}. |  |
|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | −log⁡(CLOSE\displaystyle-\log\Big( | passKumaraswamy⁡(α,β)​@​k\displaystyle\operatorname{pass_{\operatorname{Kumaraswamy(\alpha,\,\beta)}}@k} | )\displaystyle\Big) | ∝k−α.\displaystyle\propto k^{-\alpha}. |  |
|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | −log⁡(CLOSE\displaystyle-\log\Big( | passContinuousBernoulli⁡(λ<1/2)​@​k\displaystyle\operatorname{pass_{\operatorname{ContinuousBernoulli(\lambda<1/2)}}@k} | )\displaystyle\Big) | ∝k−1.\displaystyle\propto k^{-1}. |  |
|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | −log⁡(CLOSE\displaystyle-\log\Big( | passReciprocal⁡(0<α<β<1)​@​k\displaystyle\operatorname{pass_{\operatorname{Reciprocal(0<\alpha<\beta<1)}}@k} | OPEN)∝\displaystyle\Big)\propto | (1−α)kk.\displaystyle\frac{(1-\alpha)^{k}}{k}. |  |

To test this understanding, we examined whether the data of [Brown et al. (2024)](#bib.bib21) and [Hughes et al. (2024)](#bib.bib54) had per-problem single-attempt success rate distributions that matched one of these simple distributions (Fig. [4](#S2.F4 "Figure 4 ‣ 2 Should Power Law Scaling Be Expected?")). We found that the distributions could indeed be well fit by a 3-parameter Kuamraswamy⁡(α,β,a=0,c)\operatorname{Kuamraswamy}(\alpha,\beta,a=0,c) distribution with scale parameter cc (Fig. [4](#S2.F4 "Figure 4 ‣ 2 Should Power Law Scaling Be Expected?"), black dashed lines); we found the scale parameter was critical to obtain good fits because the standard 2-parameter Kumaraswamy distribution is supported on (0,1)(0,1) whereas most single-attempt success distributions have a smaller maximum such as 0.010.01 or 0.10.1.

More generally, what are the distributional properties that create such power law scaling and that set the specific power law exponent?
As we now show, the negative log average success rate will exhibit power law scaling in kk with exponent bb if and only if the distribution over problems of single-attempt success probabilities itself behaves like a power law near 00 with exponent b−1b-1:

###### Theorem 3.1 (Sufficiency of Power-Law Left Tail in Distribution of Single-Attempt Success Rates).

Let 𝒟\mathcal{D} be a probability distribution on [0,1][0,1] with PDF p𝒟​(passi​@​1)p_{\mathcal{D}}(\operatorname{pass_{i}@1}).
Suppose there exist constants b>0b>0, C>0C>0, θ>0\theta>0 and δ>0\delta>0 such that,
for all 0<passi​@​1<δ0<\operatorname{pass_{i}@1}<\delta, we have

|  |  |  |
| --- | --- | --- |
|  | p𝒟​(passi​@​1)=C⋅(passi​@​1)b−1+O⁡((passi​@​1)b−1+θ).p_{\mathcal{D}}(\operatorname{pass_{i}@1})\;=\;C\cdot(\operatorname{pass_{i}@1})^{b-1}\;+\;O\bigl((\operatorname{pass_{i}@1})^{b-1+\theta}\bigr). |  |

Then, for large kk,

|  |  |  |
| --- | --- | --- |
|  | −log⁡(pass𝒟​@​k)∼C​Γ​(b)​k−b.-\log\big(\operatorname{pass_{\mathcal{D}}@k}\big)\;\sim\;C\,\Gamma(b)\;k^{-b}. |  |

###### Theorem 3.2 (Necessity of Power-Law Left Tail in Distribution of Single-Attempt Success Rates).

Let 𝒟\mathcal{D} be a distribution over passi​@​1∈[0,1]\operatorname{pass_{i}@1}\in[0,1] with PDF p𝒟​(passi​@​1)p_{\mathcal{D}}(\operatorname{pass_{i}@1}).
Suppose there exist constants b>0b>0 and A>0A>0 such that for large kk,

|  |  |  |
| --- | --- | --- |
|  | −log⁡(pass𝒟​@​k)∼A​k−b.-\log\big(\operatorname{pass_{\mathcal{D}}@k}\big)\sim A\,k^{-b}. |  |

Then, under mild regularity assumptions, the probability density must satisfy

|  |  |  |
| --- | --- | --- |
|  | p𝒟​(passi​@​1)∼AΓ⁡(b)​(passi​@​1)b−1as ​passi​@​1→0+.p_{\mathcal{D}}(\operatorname{pass_{i}@1})\;\sim\;\frac{A}{\Gamma(b)}\,(\operatorname{pass_{i}@1})^{b-1}\quad\text{as }\operatorname{pass_{i}@1}\to 0^{+}. |  |

In Fig. [2](#S1.F2 "Figure 2 ‣ 1 Introduction"), we illustrate this connection schematically.
For proofs, see Appendices [E](#A5.SSx1 "Sufficient Condition for Power-Law Scaling in Negative Log of Aggregate Success ‣ Appendix E Aggregate Power Laws from a Probability Distribution over Exponential Functions") and [E.9](#A5.SS9 "E.9 Necessary Condition for Power Law Scaling from Distribution over pass_i⁢@⁢1 ‣ Appendix E Aggregate Power Laws from a Probability Distribution over Exponential Functions").
These results clarify that whenever −log⁡(pass𝒟​@​k)-\log(\operatorname{pass_{\mathcal{D}}@k}) exhibits power-law decay in kk with exponent bb, the distribution over problems of single-attempt success rates *must* have “polynomial weight” near passi​@​1=0\operatorname{pass_{i}@1}=0, i.e. p𝒟​(p)=Θ⁡(pb−1)p_{\mathcal{D}}(p)=\Theta(p^{\,b-1}).

To offer intuition, we know that each problem is being solved by the model (or equivalently, each prompt is jailbreaking the model) exponentially quickly.
If one looks across all problems in the benchmark, some have passi​@​1\operatorname{pass_{i}@1} so small that they remain unsolved for many, many attempts.
Whether these “tiny-passi​@​1\operatorname{pass_{i}@1}" problems still matter at large kk depends on how *many* such problems there are.
Polynomial density near 00 “piles up" enough hard problems in just the right way such that even though each of those problems is being solved exponentially quickly, the *aggregate* success rate over problems decreases at only a power-law rate in kk.
A more succinct mathematical summary is that, for a compound binomial distribution, the lower tail probability controls the upper tail of the marginal survivor function.

## 4 Lack of Distributional Structure Explains Deviations from Power Law Scaling

![Refer to caption](2502.17578v1/figures/92_schematic_distributional_fitting_attempt2/distributional_fitting_schematic.png)

Figure 5: Schematic: Two Estimators of Power Law Parameters for Scaling Inference Compute via Repeat Sampling. (A) Both estimators begin by generating many samples per prompt, then computing the number of successes per prompt. In the standard least squares power law parameter estimator (top), (B) passi​@​k\operatorname{pass_{i}@k} is estimated for each ii-th problem at multiple kk values, then (C) averaged over problems and fit with linear regression in log-log space.
In the distributional power law parameter estimator (bottom), (D) a distribution 𝒟\mathcal{D} is fit to estimates of passi​@​1\operatorname{pass_{i}@1}, then (E) the single-attempt success probability distribution is used to simulate pass𝒟​@​k\operatorname{pass_{\mathcal{D}}@k} at arbitrary kk values for linear regression in log-log space.

Notably, previous papers observed that not every model exhibits power law scaling in every setting. To highlight one, [Hughes et al. (2024)](#bib.bib54) observed that when jailbreaking Meta’s Llama 3 8B Instruction Tuned (IT) model [Grattafiori et al. (2024)](#bib.bib45), the −log⁡(ASR𝒟​@​k)-\log(\operatorname{ASR_{\mathcal{D}}@k}) fell faster than any power law (Fig. [1](#S1.F1 "Figure 1 ‣ 1 Introduction")), i.e., the ASR𝒟​@​k\operatorname{ASR_{\mathcal{D}}@k} rose much more quickly than the other frontier AI systems. Based on our mathematical insights and the empirical per-problem single-attempt attack success rates (Fig. [4](#S2.F4 "Figure 4 ‣ 2 Should Power Law Scaling Be Expected?")), we can understand why: Llama 3 8B IT could be successfully jailbroken on every prompt within the permitted sampling budget and thus had no heavy left tail necessary to create the aggregate power law scaling.

Figure 6: Comparing Estimators of Power Law Exponents. We compare two estimators of the power law exponent bb in −log⁡(pass𝒟​@​k)≈a​k−b-\log(\operatorname{pass_{\mathcal{D}}@k})\approx ak^{-b}\;: (1) the standard least-squares estimator between kk and −log⁡(pass𝒟​@​k)-\log(\operatorname{pass_{\mathcal{D}}@k}) in log-log space, and (2) the distributional estimator of passi​@​1\operatorname{pass_{i}@1} assuming a scaled Kumaraswamy-Binomial distribution. Using all available data to fit both estimators, we find agreement between the least-squares estimate (ordinate) and the distribution-derived estimate (abscissa) for both Pythia models on MATH (left) and for frontier AI systems on HarmBench (right). For an explanation of why the two estimators match more closely for Large Language Monkeys than for Best-of-N Jailbreaking, see Appendix [A](#A1 "Appendix A Clarification of How Large Language Monkeys and Best-of-N Jailbreaking Sampled Data").

Figure 7: Comparing Two Estimators of Power Law Exponents via Backtesting. On synthetic data with known ground-truth power law a​k−ba\,k^{-b}, we compare how well the least squares and the distributional estimator recover the scaling exponent bb as measured by the relative error |b^−b|/b|\hat{b}-b|/b by backtesting: subsampling the number of problems and the number of samples per problem. We find that the distributional estimator obtains significantly better sample efficiency.

## 5 A New Distributional Estimator for Predicting Power Law Scaling

A natural consequence of this connection between the scaling of −log⁡(pass𝒟​@​k)-\log(\operatorname{pass_{\mathcal{D}}@k}) and the left tail of the distribution p𝒟​(passi​@​1)p_{\mathcal{D}}(\operatorname{pass_{i}@1}) is that the distribution of single-attempt success rates can be used to predict whether power-law scaling will appear and if so, what the intercept and exponent of the power law will be. To do this, one can fit the distribution p^𝒟​(passi​@​1)\hat{p}_{\mathcal{D}}(\operatorname{pass_{i}@1}) and then simulate how pass𝒟​@​k\operatorname{pass_{\mathcal{D}}@k} will scale with kk (Fig. [5](#S4.F5 "Figure 5 ‣ 4 Lack of Distributional Structure Explains Deviations from Power Law Scaling")) using the relationship:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | pass𝒟​@​k^​=def\displaystyle\widehat{\operatorname{pass_{\mathcal{D}}@k}}\defeq |  | (11) |
|  |  | 1−∫01(1−passi​@​1)k​p^𝒟​(passi​@​1)​d​passi​@​1.\displaystyle 1-\int_{0}^{1}(1-\operatorname{pass_{i}@1})^{k}\,\hat{p}_{\mathcal{D}}(\operatorname{pass_{i}@1})\,\operatorname{d\,pass_{i}@1}. |  |

To empirically test this claim, we compared the standard least squares regression estimator (in log-log space) ([Hoffmann et al., 2022](#bib.bib52); [Caballero et al., 2022](#bib.bib24); [Besiroglu et al., 2024b](#bib.bib13)) against a distributional estimator.
To motivate our distributional estimator, we first need explain a key obstacle and how the distributional estimator overcomes it.
The obstacle is that there are problems or prompts whose single-attempt success probabilities passi​@​1\operatorname{pass_{i}@1} lie between (0,1/Number of Samples)(0,1/\text{Number of Samples}) such that, due to finite sampling, we lack the resolution to measure.
While we do not know the true single-attempt success probability for the problems that lie in this interval, we do know how many problems fall into this left tail bucket, and we can fit a distribution’s parameters such that the distribution’s probability mass in the interval (0,1/Number of Samples)(0,1/\text{Number of Samples}) matches the empirical fraction of problems in this tail bucket. Thus, our distributional estimator works by first selecting a distribution (e.g., a scaled 3-parameter Beta distribution), discretizing the distribution according to the sampling resolution 1/Number of Samples1/\text{Number of Samples} and performing maximum likelihood estimation under the discretized distribution’s probability mass function.

We tested this distributional estimator in two different ways. First, focusing on Large Language Monkeys, we used all available real data from all problems and all samples per problem to compare the standard least squares regression estimator against the distributional estimator.
We found close agreement between the two estimators (Fig. [6](#S4.F6 "Figure 6 ‣ 4 Lack of Distributional Structure Explains Deviations from Power Law Scaling")), giving us a sense that the two estimators yield reasonably consistent estimates under large sampling budgets.

Second, the distributional estimator also comes with another benefit: it directly provides an estimate of the power law’s exponent bb in a​k−ba\,k^{-b}. Estimating the power law’s exponent is especially valuable because the exponent dictates how success rates are improving with increasing inference compute. To test how the distributional estimator and least squares estimator compare at recovering the true asymptotic power law exponent, we generated synthetic data so that we would have ground-truth knowledge of the true power law exponent, then backtested how the two scaling estimators compare at recovering the true exponent ([Alabdulmohsin et al., 2022a](#bib.bib3); [Owen, 2024](#bib.bib79)) by subsampling data with fewer problems and fewer samples per problem.
We found that the distributional estimator obtains significantly better sample efficiency, with approximately an order of magnitude lower relative error =def|b^−b|/b\defeq|\hat{b}-b|/b compared with the least squares estimator (Fig. [7](#S4.F7 "Figure 7 ‣ 4 Lack of Distributional Structure Explains Deviations from Power Law Scaling")), or equivalently, ∼2−4{\sim}2-4 orders of magnitude less inference-compute. The distributional estimator performs well even under distributional mismatch.

## 6 Related Work

Research into scaling laws of deep neural networks has a rich history spanning theoretical foundations, empirical validations, and diverse applications. The earliest investigations discovered power law scaling in simple machine learning settings ([Barkai et al., 1993](#bib.bib11); [Mhaskar, 1996](#bib.bib72); [Pinkus, 1999](#bib.bib82)). However, the modern era of scaling laws began with breakthrough studies in neural language models ([Hestness et al., 2017](#bib.bib50); [Kaplan et al., 2020](#bib.bib59); [Brown et al., 2020b](#bib.bib23)), catalyzing extensive research across multiple directions.
The theoretical understanding of scaling laws has advanced significantly ([Spigler et al., 2020](#bib.bib101); [Bousquet et al., 2020](#bib.bib19); [Hutter, 2021](#bib.bib55); [Sharma & Kaplan, 2022](#bib.bib97); [Maloney et al., 2022](#bib.bib67); [Roberts et al., 2022](#bib.bib86); [Bahri et al., 2024](#bib.bib10); [Michaud et al., 2024](#bib.bib73); [Paquette et al., 2024](#bib.bib81); [Atanasov et al., 2024](#bib.bib8); [Bordelon et al., 2024a](#bib.bib17); [Bordelon et al., 2024b](#bib.bib18); [Lin et al., 2024](#bib.bib65); [Brill, 2024](#bib.bib20)), complemented by comprehensive empirical studies ([Rosenfeld et al., 2020](#bib.bib88); [Henighan et al., 2020](#bib.bib47); [Gordon et al., 2021](#bib.bib44); [Tay et al., 2021](#bib.bib105); [Ghorbani et al., 2021](#bib.bib43); [Tay et al., 2022b](#bib.bib107); [Zhai et al., 2022](#bib.bib116); [Alabdulmohsin et al., 2022b](#bib.bib4); [Dehghani et al., 2023](#bib.bib31); [Bachmann et al., 2023](#bib.bib9)).
In the context of language models, researchers have explored scaling behaviors in various aspects: context length ([Xiong et al., 2023](#bib.bib115)), in-context learning ([Chan et al., 2022](#bib.bib26); [Agarwal et al., 2024](#bib.bib1); [Arora et al., 2024](#bib.bib7)), vocabulary size ([Tao et al., 2024](#bib.bib104)), and jailbreaking attempts ([Anil et al., 2024](#bib.bib6); [Hughes et al., 2024](#bib.bib54)). Studies have also investigated scaling dynamics in fine-tuning ([Kalajdzievski, 2024](#bib.bib58); [Zhang et al., 2024](#bib.bib117)), transfer learning ([Hernandez et al., 2021](#bib.bib48)), and the impact of repeated data ([Hernandez et al., 2022](#bib.bib49); [Muennighoff et al., 2023](#bib.bib75)).
Architectural considerations have been extensively studied, including network design ([Tay et al., 2022a](#bib.bib106); [Clark et al., 2022](#bib.bib30)), nested models ([Kudugunta et al., 2023](#bib.bib61)), pruning strategies ([Rosenfeld et al., 2021](#bib.bib89)), and precision requirements ([Dettmers & Zettlemoyer, 2023](#bib.bib32); [Kumar et al., 2024](#bib.bib63); [Sun et al., 2025](#bib.bib103)). Research has also addressed multimodal extensions ([Aghajanyan et al., 2023](#bib.bib2); [Cherti et al., 2023](#bib.bib29)) and inference optimization ([Sardana et al., 2023](#bib.bib91); [Brown et al., 2024](#bib.bib21); [Snell et al., 2024a](#bib.bib98); [Wu et al., 2024](#bib.bib114); [Chen et al., 2024](#bib.bib28)).
The field has expanded to encompass diverse domains including reinforcement learning (both single-agent ([Jones, 2021](#bib.bib57); [Hilton et al., 2023](#bib.bib51); [Neumann & Gros, 2024](#bib.bib77)) and multi-agent ([Neumann & Gros, 2022](#bib.bib76))), graph networks ([Liu et al., 2024](#bib.bib66)), diffusion models ([Mei et al., 2024](#bib.bib71); [Liang et al., 2024](#bib.bib64)), and associative memory models ([Romani et al., 2013](#bib.bib87); [Cabannes et al., 2024](#bib.bib25); [Schaeffer et al., 2024c](#bib.bib96)).
Recent work has explored emerging phenomena such as inverse scaling ([McKenzie et al., 2024](#bib.bib70)), unique functional forms ([Caballero et al., 2022](#bib.bib24)), scaling patterns across model families ([Ruan et al., 2024](#bib.bib90); [Polo et al., 2024](#bib.bib83)), and downstream capabilities ([Srivastava et al., 2023](#bib.bib102); [Wei et al., 2022a](#bib.bib111); [Hu et al., 2024](#bib.bib53); [Schaeffer et al., 2024b](#bib.bib95); [Snell et al., 2024b](#bib.bib99); [Wu & Lo, 2024](#bib.bib113)). Researchers have also investigated critical challenges including data contamination ([Schaeffer, 2023](#bib.bib92); [Jiang et al., 2024](#bib.bib56); [Dominguez-Olmedo et al., 2024](#bib.bib34)), model-data feedback loops ([Dohmatob et al., 2024](#bib.bib33); [Gerstgrasser et al., 2024](#bib.bib42); [Kazdan et al., 2024](#bib.bib60)), and overtraining effects ([Gao et al., 2023](#bib.bib40); [Gadre et al., 2024](#bib.bib38)). Additional contributions include studies in sparse autoencoders ([Gao et al., 2024](#bib.bib41)), biologically-plausible backpropagation ([Filipovich et al., 2022](#bib.bib37)), and self-supervised learning for vision ([Schaeffer et al., 2024a](#bib.bib94)).
Recent efforts have also focused on reconciling apparent contradictions in scaling behaviors ([Besiroglu et al., 2024b](#bib.bib13); [Porian et al., 2024](#bib.bib84)).

## 7 Discussion and Future Directions

This work advances our mathematical understanding of how and why language model performance improves with additional inference compute through repeat sampling. By establishing rigorous theoretical foundations for these empirically-observed power laws, our work provides practitioners with principled ways to understand and predict model performance when scaling inference compute. The distributional perspective we develop explains previously puzzling deviations from power law scaling and enables more efficient estimation of scaling parameters.

Two related questions are *why* such distributional structure exists in the single-attempt success rates and whether one should expect such structure to appear in future benchmarks. We conjecture there are at least two reasons: (1) benchmark design, in that benchmarks are intentionally crafted that problems have a spread of difficulty without being too easy or too hard, and (2) selection bias, in that more interesting patterns such as power law scaling are more likely to garner more interest from the research community.

Despite focusing on scaling inference compute, our paper contributes is a new hypothesis for an open question in scaling pretraining compute: why are neural scaling laws power laws? Just as the scaling behavior of −log⁡(pass𝒟​@​k)-\log(\operatorname{pass_{\mathcal{D}}@k}) only becomes clear for large kk, so too might the scaling behavior of pretraining cross entropy with pretraining compute CC.
Specifically, suppose the pretraining cross entropy ℒ\mathcal{L} as a function of pretraining compute CC is a sum of many functions which decay at different rates:

|  |  |  |
| --- | --- | --- |
|  | ℒ⁡(C)=ω⁡(1Cα)+ACα+o⁡(1Cα),\mathcal{L}(C)=\omega\Big(\frac{1}{C^{\alpha}}\Big)+\frac{A}{C^{\alpha}}+o\Big(\frac{1}{C^{\alpha}}\Big), |  |

where α\alpha is the smallest (positive) polynomial exponent and ω⁡(1/Cα)\omega(1/C^{\alpha}) represents functions that decay more slowly than any polynomial. Initially, for small CC, the dominant term may be unclear, but as pretraining compute is scaled up across 8−108-10 orders of magnitude, the leading order term dominates and an approximate power law emerges:

|  |  |  |
| --- | --- | --- |
|  | ℒ⁡(C)≈const+ACα+0 as C→∞.\mathcal{L}(C)\approx\text{const}+\frac{A}{C^{\alpha}}+0\quad\text{ as }\quad C\rightarrow\infty. |  |

Thus, a power law relationship may only be reasonable for sufficiently large pretraining compute CC, which in turn may require excluding the lowest pretraining compute models in order to obtain good predictions, justifying a widespread empirical practice ([Kaplan et al., 2020](#bib.bib59)). We designate possible functions hiding in ω⁡(1/Cα)\omega(1/C^{\alpha}) and o⁡(1/Cα)o(1/C^{\alpha}) as the dark matter of neural scaling laws.

## Acknowledgments

Redacted for blind review.

## Impact Statement

Our findings have important practical implications for the deployment of large language models, as they can help organizations more accurately forecast compute requirements and make informed trade-offs between model size, inference costs, and performance targets. The mathematical framework we develop could also generalize beyond language models to other domains where similar scaling phenomena emerge. While our work is primarily theoretical, we acknowledge that advances in language model capabilities can have broad societal impacts. We hope that better understanding these fundamental scaling behaviors will help the research community develop more efficient and reliable AI systems.

## References

- Agarwal et al. (2024)

  Agarwal, R., Singh, A., Zhang, L. M., Bohnet, B., Rosias, L., Chan, S. C., Zhang, B., Anand, A., Abbas, Z., Nova, A., Co-Reyes, J. D., Chu, E., Behbahani, F., Faust, A., and Larochelle, H.
  Many-shot in-context learning.
  In *The Thirty-eighth Annual Conference on Neural Information Processing Systems*, 2024.
  URL <https://openreview.net/forum?id=AB6XpMzvqH>.
- Aghajanyan et al. (2023)

  Aghajanyan, A., Yu, L., Conneau, A., Hsu, W.-N., Hambardzumyan, K., Zhang, S., Roller, S., Goyal, N., Levy, O., and Zettlemoyer, L.
  Scaling laws for generative mixed-modal language models.
  In *International Conference on Machine Learning*, pp. 265–279. PMLR, 2023.
- Alabdulmohsin et al. (2022a)

  Alabdulmohsin, I., Neyshabur, B., and Zhai, X.
  Revisiting neural scaling laws in language and vision, 2022a.
  URL <https://arxiv.org/abs/2209.06640>.
- Alabdulmohsin et al. (2022b)

  Alabdulmohsin, I. M., Neyshabur, B., and Zhai, X.
  Revisiting neural scaling laws in language and vision.
  *Advances in Neural Information Processing Systems*, 35:22300–22312, 2022b.
- Anderljung et al. (2023)

  Anderljung, M., Barnhart, J., Korinek, A., Leung, J., O’Keefe, C., Whittlestone, J., Avin, S., Brundage, M., Bullock, J., Cass-Beggs, D., Chang, B., Collins, T., Fist, T., Hadfield, G., Hayes, A., Ho, L., Hooker, S., Horvitz, E., Kolt, N., Schuett, J., Shavit, Y., Siddarth, D., Trager, R., and Wolf, K.
  Frontier ai regulation: Managing emerging risks to public safety, 2023.
  URL <https://arxiv.org/abs/2307.03718>.
- Anil et al. (2024)

  Anil, C., DURMUS, E., Rimsky, N., Sharma, M., Benton, J., Kundu, S., Batson, J., Tong, M., Mu, J., Ford, D. J., Mosconi, F., Agrawal, R., Schaeffer, R., Bashkansky, N., Svenningsen, S., Lambert, M., Radhakrishnan, A., Denison, C., Hubinger, E. J., Bai, Y., Bricken, T., Maxwell, T., Schiefer, N., Sully, J., Tamkin, A., Lanham, T., Nguyen, K., Korbak, T., Kaplan, J., Ganguli, D., Bowman, S. R., Perez, E., Grosse, R. B., and Duvenaud, D.
  Many-shot jailbreaking.
  In *The Thirty-eighth Annual Conference on Neural Information Processing Systems*, 2024.
  URL <https://openreview.net/forum?id=cw5mgd71jW>.
- Arora et al. (2024)

  Arora, A., Jurafsky, D., Potts, C., and Goodman, N. D.
  Bayesian scaling laws for in-context learning, 2024.
  URL <https://arxiv.org/abs/2410.16531>.
- Atanasov et al. (2024)

  Atanasov, A., Zavatone-Veth, J. A., and Pehlevan, C.
  Scaling and renormalization in high-dimensional regression.
  *arXiv preprint arXiv:2405.00592*, 2024.
- Bachmann et al. (2023)

  Bachmann, G., Anagnostidis, S., and Hofmann, T.
  Scaling mlps: A tale of inductive bias, 2023.
  URL <https://arxiv.org/abs/2306.13575>.
- Bahri et al. (2024)

  Bahri, Y., Dyer, E., Kaplan, J., Lee, J., and Sharma, U.
  Explaining neural scaling laws.
  *Proceedings of the National Academy of Sciences*, 121(27):e2311878121, 2024.
- Barkai et al. (1993)

  Barkai, N., Seung, H. S., and Sompolinsky, H.
  Scaling laws in learning of classification tasks.
  *Physical review letters*, 70(20):3167, 1993.
- Besiroglu et al. (2024a)

  Besiroglu, T., Emery-Xu, N., and Thompson, N.
  Economic impacts of ai-augmented r&d.
  *Research Policy*, 53(7):105037, 2024a.
- Besiroglu et al. (2024b)

  Besiroglu, T., Erdil, E., Barnett, M., and You, J.
  Chinchilla scaling: A replication attempt, 2024b.
  URL <https://arxiv.org/abs/2404.10102>.
- Biderman et al. (2023)

  Biderman, S., Schoelkopf, H., Anthony, Q. G., Bradley, H., O’Brien, K., Hallahan, E., Khan, M. A., Purohit, S., Prashanth, U. S., Raff, E., et al.
  Pythia: A suite for analyzing large language models across training and scaling.
  In *International Conference on Machine Learning*, pp. 2397–2430. PMLR, 2023.
- Bochud & Challet (2006)

  Bochud, T. and Challet, D.
  Optimal approximations of power-laws with exponentials, 2006.
  URL <https://arxiv.org/abs/physics/0605149>.
- Bommasani et al. (2021)

  Bommasani, R., Hudson, D. A., Adeli, E., Altman, R., Arora, S., von Arx, S., Bernstein, M. S., Bohg, J., Bosselut, A., Brunskill, E., et al.
  On the opportunities and risks of foundation models.
  *arXiv preprint arXiv:2108.07258*, 2021.
- Bordelon et al. (2024a)

  Bordelon, B., Atanasov, A., and Pehlevan, C.
  A dynamical model of neural scaling laws.
  *arXiv preprint arXiv:2402.01092*, 2024a.
- Bordelon et al. (2024b)

  Bordelon, B., Atanasov, A., and Pehlevan, C.
  How feature learning can improve neural scaling laws.
  *arXiv preprint arXiv:2409.17858*, 2024b.
- Bousquet et al. (2020)

  Bousquet, O., Hanneke, S., Moran, S., van Handel, R., and Yehudayoff, A.
  A theory of universal learning, 2020.
  URL <https://arxiv.org/abs/2011.04483>.
- Brill (2024)

  Brill, A.
  Neural scaling laws rooted in the data distribution.
  *arXiv preprint arXiv:2412.07942*, 2024.
- Brown et al. (2024)

  Brown, B., Juravsky, J., Ehrlich, R., Clark, R., Le, Q. V., Ré, C., and Mirhoseini, A.
  Large language monkeys: Scaling inference compute with repeated sampling, 2024.
  URL <https://arxiv.org/abs/2407.21787>.
- Brown et al. (2020a)

  Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., et al.
  Language models are few-shot learners.
  *Advances in neural information processing systems*, 33:1877–1901, 2020a.
- Brown et al. (2020b)

  Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D. M., Wu, J., Winter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M., Gray, S., Chess, B., Clark, J., Berner, C., McCandlish, S., Radford, A., Sutskever, I., and Amodei, D.
  Language models are few-shot learners, 2020b.
  URL <https://arxiv.org/abs/2005.14165>.
- Caballero et al. (2022)

  Caballero, E., Gupta, K., Rish, I., and Krueger, D.
  Broken neural scaling laws.
  *arXiv preprint arXiv:2210.14891*, 2022.
- Cabannes et al. (2024)

  Cabannes, V., Dohmatob, E., and Bietti, A.
  Scaling laws for associative memories, 2024.
  URL <https://arxiv.org/abs/2310.02984>.
- Chan et al. (2022)

  Chan, S., Santoro, A., Lampinen, A., Wang, J., Singh, A., Richemond, P., McClelland, J., and Hill, F.
  Data distributional properties drive emergent in-context learning in transformers.
  In Koyejo, S., Mohamed, S., Agarwal, A., Belgrave, D., Cho, K., and Oh, A. (eds.), *Advances in Neural Information Processing Systems*, volume 35, pp. 18878–18891. Curran Associates, Inc., 2022.
  URL <https://proceedings.neurips.cc/paper_files/paper/2022/file/77c6ccacfd9962e2307fc64680fc5ace-Paper-Conference.pdf>.
- Chen et al. (2021)

  Chen, M., Tworek, J., Jun, H., Yuan, Q., de Oliveira Pinto, H. P., Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman, G., Ray, A., Puri, R., Krueger, G., Petrov, M., Khlaaf, H., Sastry, G., Mishkin, P., Chan, B., Gray, S., Ryder, N., Pavlov, M., Power, A., Kaiser, L., Bavarian, M., Winter, C., Tillet, P., Such, F. P., Cummings, D., Plappert, M., Chantzis, F., Barnes, E., Herbert-Voss, A., Guss, W. H., Nichol, A., Paino, A., Tezak, N., Tang, J., Babuschkin, I., Balaji, S., Jain, S., Saunders, W., Hesse, C., Carr, A. N., Leike, J., Achiam, J., Misra, V., Morikawa, E., Radford, A., Knight, M., Brundage, M., Murati, M., Mayer, K., Welinder, P., McGrew, B., Amodei, D., McCandlish, S., Sutskever, I., and Zaremba, W.
  Evaluating large language models trained on code, 2021.
  URL <https://arxiv.org/abs/2107.03374>.
- Chen et al. (2024)

  Chen, Y., Pan, X., Li, Y., Ding, B., and Zhou, J.
  A simple and provable scaling law for the test-time compute of large language models, 2024.
  URL <https://arxiv.org/abs/2411.19477>.
- Cherti et al. (2023)

  Cherti, M., Beaumont, R., Wightman, R., Wortsman, M., Ilharco, G., Gordon, C., Schuhmann, C., Schmidt, L., and Jitsev, J.
  Reproducible scaling laws for contrastive language-image learning.
  In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, pp. 2818–2829, 2023.
- Clark et al. (2022)

  Clark, A., de Las Casas, D., Guy, A., Mensch, A., Paganini, M., Hoffmann, J., Damoc, B., Hechtman, B., Cai, T., Borgeaud, S., et al.
  Unified scaling laws for routed language models.
  In *International conference on machine learning*, pp. 4057–4086. PMLR, 2022.
- Dehghani et al. (2023)

  Dehghani, M., Djolonga, J., Mustafa, B., Padlewski, P., Heek, J., Gilmer, J., Steiner, A. P., Caron, M., Geirhos, R., Alabdulmohsin, I., et al.
  Scaling vision transformers to 22 billion parameters.
  In *International Conference on Machine Learning*, pp. 7480–7512. PMLR, 2023.
- Dettmers & Zettlemoyer (2023)

  Dettmers, T. and Zettlemoyer, L.
  The case for 4-bit precision: k-bit inference scaling laws.
  In *International Conference on Machine Learning*, pp. 7750–7774. PMLR, 2023.
- Dohmatob et al. (2024)

  Dohmatob, E., Feng, Y., Yang, P., Charton, F., and Kempe, J.
  A tale of tails: Model collapse as a change of scaling laws, 2024.
  URL <https://arxiv.org/abs/2402.07043>.
- Dominguez-Olmedo et al. (2024)

  Dominguez-Olmedo, R., Dorner, F. E., and Hardt, M.
  Training on the test task confounds evaluation and emergence, 2024.
  URL <https://arxiv.org/abs/2407.07890>.
- Elkies (2016)

  Elkies, N. D.
  Is there a way to express an power law decay as a series of exponentials?
  MathOverflow, 2016.
  URL <https://mathoverflow.net/q/251661>.
  URL:https://mathoverflow.net/q/251661 (version: 2016-10-08).
- Eloundou et al. (2023)

  Eloundou, T., Manning, S., Mishkin, P., and Rock, D.
  Gpts are gpts: An early look at the labor market impact potential of large language models, 2023.
  URL <https://arxiv.org/abs/2303.10130>.
- Filipovich et al. (2022)

  Filipovich, M. J., Cappelli, A., Hesslow, D., and Launay, J.
  Scaling laws beyond backpropagation, 2022.
  URL <https://arxiv.org/abs/2210.14593>.
- Gadre et al. (2024)

  Gadre, S. Y., Smyrnis, G., Shankar, V., Gururangan, S., Wortsman, M., Shao, R., Mercat, J., Fang, A., Li, J., Keh, S., et al.
  Language models scale reliably with over-training and on downstream tasks.
  *arXiv preprint arXiv:2403.08540*, 2024.
- Ganguli et al. (2022)

  Ganguli, D., Hernandez, D., Lovitt, L., Askell, A., Bai, Y., Chen, A., Conerly, T., Dassarma, N., Drain, D., Elhage, N., et al.
  Predictability and surprise in large generative models.
  In *2022 ACM Conference on Fairness, Accountability, and Transparency*, pp. 1747–1764, 2022.
- Gao et al. (2023)

  Gao, L., Schulman, J., and Hilton, J.
  Scaling laws for reward model overoptimization.
  In Krause, A., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), *Proceedings of the 40th International Conference on Machine Learning*, volume 202 of *Proceedings of Machine Learning Research*, pp. 10835–10866. PMLR, 23–29 Jul 2023.
  URL <https://proceedings.mlr.press/v202/gao23h.html>.
- Gao et al. (2024)

  Gao, L., la Tour, T. D., Tillman, H., Goh, G., Troll, R., Radford, A., Sutskever, I., Leike, J., and Wu, J.
  Scaling and evaluating sparse autoencoders.
  *arXiv preprint arXiv:2406.04093*, 2024.
- Gerstgrasser et al. (2024)

  Gerstgrasser, M., Schaeffer, R., Dey, A., Rafailov, R., Sleight, H., Hughes, J., Korbak, T., Agrawal, R., Pai, D., Gromov, A., Roberts, D. A., Yang, D., Donoho, D. L., and Koyejo, S.
  Is model collapse inevitable? breaking the curse of recursion by accumulating real and synthetic data, 2024.
  URL <https://arxiv.org/abs/2404.01413>.
- Ghorbani et al. (2021)

  Ghorbani, B., Firat, O., Freitag, M., Bapna, A., Krikun, M., Garcia, X., Chelba, C., and Cherry, C.
  Scaling laws for neural machine translation.
  In *International Conference on Learning Representations*, 2021.
- Gordon et al. (2021)

  Gordon, M. A., Duh, K., and Kaplan, J.
  Data and parameter scaling laws for neural machine translation.
  In Moens, M.-F., Huang, X., Specia, L., and Yih, S. W.-t. (eds.), *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*, pp. 5915–5922, Online and Punta Cana, Dominican Republic, November 2021. Association for Computational Linguistics.
  doi: 10.18653/v1/2021.emnlp-main.478.
  URL <https://aclanthology.org/2021.emnlp-main.478>.
- Grattafiori et al. (2024)

  Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Letman, A., Mathur, A., Schelten, A., Vaughan, A., Yang, A., Fan, A., Goyal, A., Hartshorn, A., Yang, A., Mitra, A., Sravankumar, A., Korenev, A., Hinsvark, A., Rao, A., Zhang, A., Rodriguez, A., Gregerson, A., Spataru, A., Roziere, B., Biron, B., Tang, B., Chern, B., Caucheteux, C., Nayak, C., Bi, C., Marra, C., McConnell, C., Keller, C., Touret, C., Wu, C., Wong, C., Ferrer, C. C., Nikolaidis, C., Allonsius, D., Song, D., Pintz, D., Livshits, D., Wyatt, D., Esiobu, D., Choudhary, D., Mahajan, D., Garcia-Olano, D., Perino, D., Hupkes, D., Lakomkin, E., AlBadawy, E., Lobanova, E., Dinan, E., Smith, E. M., Radenovic, F., Guzmán, F., Zhang, F., Synnaeve, G., Lee, G., Anderson, G. L., Thattai, G., Nail, G., Mialon, G., Pang, G., Cucurell, G., Nguyen, H., Korevaar, H., Xu, H., Touvron, H., Zarov, I., Ibarra, I. A., Kloumann, I., Misra, I., Evtimov, I., Zhang, J., Copet, J., Lee, J., Geffert, J., Vranes, J., Park, J., Mahadeokar, J.,
  Shah, J., van der Linde, J., Billock, J., Hong, J., Lee, J., Fu, J., Chi, J., Huang, J., Liu, J., Wang, J., Yu, J., Bitton, J., Spisak, J., Park, J., Rocca, J., Johnstun, J., Saxe, J., Jia, J., Alwala, K. V., Prasad, K., Upasani, K., Plawiak, K., Li, K., Heafield, K., Stone, K., El-Arini, K., Iyer, K., Malik, K., Chiu, K., Bhalla, K., Lakhotia, K., Rantala-Yeary, L., van der Maaten, L., Chen, L., Tan, L., Jenkins, L., Martin, L., Madaan, L., Malo, L., Blecher, L., Landzaat, L., de Oliveira, L., Muzzi, M., Pasupuleti, M., Singh, M., Paluri, M., Kardas, M., Tsimpoukelli, M., Oldham, M., Rita, M., Pavlova, M., Kambadur, M., Lewis, M., Si, M., Singh, M. K., Hassan, M., Goyal, N., Torabi, N., Bashlykov, N., Bogoychev, N., Chatterji, N., Zhang, N., Duchenne, O., Çelebi, O., Alrassy, P., Zhang, P., Li, P., Vasic, P., Weng, P., Bhargava, P., Dubal, P., Krishnan, P., Koura, P. S., Xu, P., He, Q., Dong, Q., Srinivasan, R., Ganapathy, R., Calderer, R., Cabral, R. S., Stojnic, R., Raileanu, R., Maheswari, R., Girdhar,
  R., Patel, R., Sauvestre, R., Polidoro, R., Sumbaly, R., Taylor, R., Silva, R., Hou, R., Wang, R., Hosseini, S., Chennabasappa, S., Singh, S., Bell, S., Kim, S. S., Edunov, S., Nie, S., Narang, S., Raparthy, S., Shen, S., Wan, S., Bhosale, S., Zhang, S., Vandenhende, S., Batra, S., Whitman, S., Sootla, S., Collot, S., Gururangan, S., Borodinsky, S., Herman, T., Fowler, T., Sheasha, T., Georgiou, T., Scialom, T., Speckbacher, T., Mihaylov, T., Xiao, T., Karn, U., Goswami, V., Gupta, V., Ramanathan, V., Kerkez, V., Gonguet, V., Do, V., Vogeti, V., Albiero, V., Petrovic, V., Chu, W., Xiong, W., Fu, W., Meers, W., Martinet, X., Wang, X., Wang, X., Tan, X. E., Xia, X., Xie, X., Jia, X., Wang, X., Goldschlag, Y., Gaur, Y., Babaei, Y., Wen, Y., Song, Y., Zhang, Y., Li, Y., Mao, Y., Coudert, Z. D., Yan, Z., Chen, Z., Papakipos, Z., Singh, A., Srivastava, A., Jain, A., Kelsey, A., Shajnfeld, A., Gangidi, A., Victoria, A., Goldstand, A., Menon, A., Sharma, A., Boesenberg, A., Baevski, A., Feinstein, A., Kallet, A.,
  Sangani, A., Teo, A., Yunus, A., Lupu, A., Alvarado, A., Caples, A., Gu, A., Ho, A., Poulton, A., Ryan, A., Ramchandani, A., Dong, A., Franco, A., Goyal, A., Saraf, A., Chowdhury, A., Gabriel, A., Bharambe, A., Eisenman, A., Yazdan, A., James, B., Maurer, B., Leonhardi, B., Huang, B., Loyd, B., Paola, B. D., Paranjape, B., Liu, B., Wu, B., Ni, B., Hancock, B., Wasti, B., Spence, B., Stojkovic, B., Gamido, B., Montalvo, B., Parker, C., Burton, C., Mejia, C., Liu, C., Wang, C., Kim, C., Zhou, C., Hu, C., Chu, C.-H., Cai, C., Tindal, C., Feichtenhofer, C., Gao, C., Civin, D., Beaty, D., Kreymer, D., Li, D., Adkins, D., Xu, D., Testuggine, D., David, D., Parikh, D., Liskovich, D., Foss, D., Wang, D., Le, D., Holland, D., Dowling, E., Jamil, E., Montgomery, E., Presani, E., Hahn, E., Wood, E., Le, E.-T., Brinkman, E., Arcaute, E., Dunbar, E., Smothers, E., Sun, F., Kreuk, F., Tian, F., Kokkinos, F., Ozgenel, F., Caggioni, F., Kanayet, F., Seide, F., Florez, G. M., Schwarz, G., Badeer, G., Swee, G., Halpern, G.,
  Herman, G., Sizov, G., Guangyi, Zhang, Lakshminarayanan, G., Inan, H., Shojanazeri, H., Zou, H., Wang, H., Zha, H., Habeeb, H., Rudolph, H., Suk, H., Aspegren, H., Goldman, H., Zhan, H., Damlaj, I., Molybog, I., Tufanov, I., Leontiadis, I., Veliche, I.-E., Gat, I., Weissman, J., Geboski, J., Kohli, J., Lam, J., Asher, J., Gaya, J.-B., Marcus, J., Tang, J., Chan, J., Zhen, J., Reizenstein, J., Teboul, J., Zhong, J., Jin, J., Yang, J., Cummings, J., Carvill, J., Shepard, J., McPhie, J., Torres, J., Ginsburg, J., Wang, J., Wu, K., U, K. H., Saxena, K., Khandelwal, K., Zand, K., Matosich, K., Veeraraghavan, K., Michelena, K., Li, K., Jagadeesh, K., Huang, K., Chawla, K., Huang, K., Chen, L., Garg, L., A, L., Silva, L., Bell, L., Zhang, L., Guo, L., Yu, L., Moshkovich, L., Wehrstedt, L., Khabsa, M., Avalani, M., Bhatt, M., Mankus, M., Hasson, M., Lennie, M., Reso, M., Groshev, M., Naumov, M., Lathi, M., Keneally, M., Liu, M., Seltzer, M. L., Valko, M., Restrepo, M., Patel, M., Vyatskov, M., Samvelyan, M., Clark,
  M., Macey, M., Wang, M., Hermoso, M. J., Metanat, M., Rastegari, M., Bansal, M., Santhanam, N., Parks, N., White, N., Bawa, N., Singhal, N., Egebo, N., Usunier, N., Mehta, N., Laptev, N. P., Dong, N., Cheng, N., Chernoguz, O., Hart, O., Salpekar, O., Kalinli, O., Kent, P., Parekh, P., Saab, P., Balaji, P., Rittner, P., Bontrager, P., Roux, P., Dollar, P., Zvyagina, P., Ratanchandani, P., Yuvraj, P., Liang, Q., Alao, R., Rodriguez, R., Ayub, R., Murthy, R., Nayani, R., Mitra, R., Parthasarathy, R., Li, R., Hogan, R., Battey, R., Wang, R., Howes, R., Rinott, R., Mehta, S., Siby, S., Bondu, S. J., Datta, S., Chugh, S., Hunt, S., Dhillon, S., Sidorov, S., Pan, S., Mahajan, S., Verma, S., Yamamoto, S., Ramaswamy, S., Lindsay, S., Lindsay, S., Feng, S., Lin, S., Zha, S. C., Patil, S., Shankar, S., Zhang, S., Zhang, S., Wang, S., Agarwal, S., Sajuyigbe, S., Chintala, S., Max, S., Chen, S., Kehoe, S., Satterfield, S., Govindaprasad, S., Gupta, S., Deng, S., Cho, S., Virk, S., Subramanian, S., Choudhury, S.,
  Goldman, S., Remez, T., Glaser, T., Best, T., Koehler, T., Robinson, T., Li, T., Zhang, T., Matthews, T., Chou, T., Shaked, T., Vontimitta, V., Ajayi, V., Montanez, V., Mohan, V., Kumar, V. S., Mangla, V., Ionescu, V., Poenaru, V., Mihailescu, V. T., Ivanov, V., Li, W., Wang, W., Jiang, W., Bouaziz, W., Constable, W., Tang, X., Wu, X., Wang, X., Wu, X., Gao, X., Kleinman, Y., Chen, Y., Hu, Y., Jia, Y., Qi, Y., Li, Y., Zhang, Y., Zhang, Y., Adi, Y., Nam, Y., Yu, Wang, Zhao, Y., Hao, Y., Qian, Y., Li, Y., He, Y., Rait, Z., DeVito, Z., Rosnbrick, Z., Wen, Z., Yang, Z., Zhao, Z., and Ma, Z.
  The llama 3 herd of models, 2024.
  URL <https://arxiv.org/abs/2407.21783>.
- Hendrycks et al. (2021)

  Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E., Song, D., and Steinhardt, J.
  Measuring mathematical problem solving with the math dataset.
  In *Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)*, 2021.
- Henighan et al. (2020)

  Henighan, T., Kaplan, J., Katz, M., Chen, M., Hesse, C., Jackson, J., Jun, H., Brown, T. B., Dhariwal, P., Gray, S., et al.
  Scaling laws for autoregressive generative modeling.
  *arXiv preprint arXiv:2010.14701*, 2020.
- Hernandez et al. (2021)

  Hernandez, D., Kaplan, J., Henighan, T., and McCandlish, S.
  Scaling laws for transfer, 2021.
  URL <https://arxiv.org/abs/2102.01293>.
- Hernandez et al. (2022)

  Hernandez, D., Brown, T., Conerly, T., DasSarma, N., Drain, D., El-Showk, S., Elhage, N., Hatfield-Dodds, Z., Henighan, T., Hume, T., et al.
  Scaling laws and interpretability of learning from repeated data.
  *arXiv preprint arXiv:2205.10487*, 2022.
- Hestness et al. (2017)

  Hestness, J., Narang, S., Ardalani, N., Diamos, G., Jun, H., Kianinejad, H., Patwary, M., Ali, M., Yang, Y., and Zhou, Y.
  Deep learning scaling is predictable, empirically.
  *arXiv preprint arXiv:1712.00409*, 2017.
- Hilton et al. (2023)

  Hilton, J., Tang, J., and Schulman, J.
  Scaling laws for single-agent reinforcement learning, 2023.
  URL <https://arxiv.org/abs/2301.13442>.
- Hoffmann et al. (2022)

  Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., de Las Casas, D., Hendricks, L. A., Welbl, J., Clark, A., Hennigan, T., Noland, E., Millican, K., van den Driessche, G., Damoc, B., Guy, A., Osindero, S., Simonyan, K., Elsen, E., Rae, J. W., Vinyals, O., and Sifre, L.
  Training compute-optimal large language models, 2022.
  URL <https://arxiv.org/abs/2203.15556>.
- Hu et al. (2024)

  Hu, S., Liu, X., Han, X., Zhang, X., He, C., Zhao, W., Lin, Y., Ding, N., Ou, Z., Zeng, G., Liu, Z., and Sun, M.
  Predicting emergent abilities with infinite resolution evaluation, 2024.
  URL <https://arxiv.org/abs/2310.03262>.
- Hughes et al. (2024)

  Hughes, J., Price, S., Lynch, A., Schaeffer, R., Barez, F., Koyejo, S., Sleight, H., Jones, E., Perez, E., and Sharma, M.
  Best-of-n jailbreaking, 2024.
  URL <https://arxiv.org/abs/2412.03556>.
- Hutter (2021)

  Hutter, M.
  Learning curve theory, 2021.
  URL <https://arxiv.org/abs/2102.04074>.
- Jiang et al. (2024)

  Jiang, M., Liu, K. Z., Zhong, M., Schaeffer, R., Ouyang, S., Han, J., and Koyejo, S.
  Investigating data contamination for pre-training language models, 2024.
  URL <https://arxiv.org/abs/2401.06059>.
- Jones (2021)

  Jones, A. L.
  Scaling scaling laws with board games.
  *arXiv preprint arXiv:2104.03113*, 2021.
- Kalajdzievski (2024)

  Kalajdzievski, D.
  Scaling laws for forgetting when fine-tuning large language models, 2024.
  URL <https://arxiv.org/abs/2401.05605>.
- Kaplan et al. (2020)

  Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., and Amodei, D.
  Scaling laws for neural language models, 2020.
  URL <https://arxiv.org/abs/2001.08361>.
- Kazdan et al. (2024)

  Kazdan, J., Schaeffer, R., Dey, A., Gerstgrasser, M., Rafailov, R., Donoho, D. L., and Koyejo, S.
  Collapse or thrive? perils and promises of synthetic data in a self-generating world, 2024.
  URL <https://arxiv.org/abs/2410.16713>.
- Kudugunta et al. (2023)

  Kudugunta, S., Kusupati, A., Dettmers, T., Chen, K., Dhillon, I., Tsvetkov, Y., Hajishirzi, H., Kakade, S., Farhadi, A., Jain, P., et al.
  Matformer: Nested transformer for elastic inference.
  *arXiv preprint arXiv:2310.07707*, 2023.
- Kulal et al. (2019)

  Kulal, S., Pasupat, P., Chandra, K., Lee, M., Padon, O., Aiken, A., and Liang, P. S.
  Spoc: Search-based pseudocode to code.
  *Advances in Neural Information Processing Systems*, 32, 2019.
- Kumar et al. (2024)

  Kumar, T., Ankner, Z., Spector, B. F., Bordelon, B., Muennighoff, N., Paul, M., Pehlevan, C., Ré, C., and Raghunathan, A.
  Scaling laws for precision.
  *arXiv preprint arXiv:2411.04330*, 2024.
- Liang et al. (2024)

  Liang, Z., He, H., Yang, C., and Dai, B.
  Scaling laws for diffusion transformers, 2024.
  URL <https://arxiv.org/abs/2410.08184>.
- Lin et al. (2024)

  Lin, L., Wu, J., Kakade, S. M., Bartlett, P. L., and Lee, J. D.
  Scaling laws in linear regression: Compute, parameters, and data.
  *arXiv preprint arXiv:2406.08466*, 2024.
- Liu et al. (2024)

  Liu, J., Mao, H., Chen, Z., Zhao, T., Shah, N., and Tang, J.
  Towards neural scaling laws on graphs, 2024.
  URL <https://arxiv.org/abs/2402.02054>.
- Maloney et al. (2022)

  Maloney, A., Roberts, D. A., and Sully, J.
  A solvable model of neural scaling laws.
  *arXiv preprint arXiv:2210.16859*, 2022.
- Maslej et al. (2024)

  Maslej, N., Fattorini, L., Perrault, R., Parli, V., Reuel, A., Brynjolfsson, E., Etchemendy, J., Ligett, K., Lyons, T., Manyika, J., Niebles, J. C., Shoham, Y., Wald, R., and Clark, J.
  Artificial intelligence index report 2024, 2024.
  URL <https://arxiv.org/abs/2405.19522>.
- Mazeika et al. (2024)

  Mazeika, M., Phan, L., Yin, X., Zou, A., Wang, Z., Mu, N., Sakhaee, E., Li, N., Basart, S., Li, B., Forsyth, D., and Hendrycks, D.
  Harmbench: A standardized evaluation framework for automated red teaming and robust refusal, 2024.
  URL <https://arxiv.org/abs/2402.04249>.
- McKenzie et al. (2024)

  McKenzie, I. R., Lyzhov, A., Pieler, M., Parrish, A., Mueller, A., Prabhu, A., McLean, E., Kirtland, A., Ross, A., Liu, A., Gritsevskiy, A., Wurgaft, D., Kauffman, D., Recchia, G., Liu, J., Cavanagh, J., Weiss, M., Huang, S., Droid, T. F., Tseng, T., Korbak, T., Shen, X., Zhang, Y., Zhou, Z., Kim, N., Bowman, S. R., and Perez, E.
  Inverse scaling: When bigger isn’t better, 2024.
  URL <https://arxiv.org/abs/2306.09479>.
- Mei et al. (2024)

  Mei, K., Tu, Z., Delbracio, M., Talebi, H., Patel, V. M., and Milanfar, P.
  Bigger is not always better: Scaling properties of latent diffusion models, 2024.
  URL <https://arxiv.org/abs/2404.01367>.
- Mhaskar (1996)

  Mhaskar, H. N.
  Neural networks for optimal approximation of smooth and analytic functions.
  *Neural computation*, 8(1):164–177, 1996.
- Michaud et al. (2024)

  Michaud, E., Liu, Z., Girit, U., and Tegmark, M.
  The quantization model of neural scaling.
  *Advances in Neural Information Processing Systems*, 36, 2024.
- mpmath development team (2023)

  mpmath development team, T.
  *mpmath: a Python library for arbitrary-precision floating-point arithmetic (version 1.3.0)*, 2023.
  http://mpmath.org/.
- Muennighoff et al. (2023)

  Muennighoff, N., Rush, A., Barak, B., Le Scao, T., Tazi, N., Piktus, A., Pyysalo, S., Wolf, T., and Raffel, C. A.
  Scaling data-constrained language models.
  *Advances in Neural Information Processing Systems*, 36:50358–50376, 2023.
- Neumann & Gros (2022)

  Neumann, O. and Gros, C.
  Scaling laws for a multi-agent reinforcement learning model.
  *arXiv preprint arXiv:2210.00849*, 2022.
- Neumann & Gros (2024)

  Neumann, O. and Gros, C.
  Alphazero neural scaling and zipf’s law: a tale of board games and power laws, 2024.
  URL <https://arxiv.org/abs/2412.11979>.
- OpenAI et al. (2024)

  OpenAI, Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F. L., Almeida, D., Altenschmidt, J., Altman, S., Anadkat, S., Avila, R., Babuschkin, I., Balaji, S., Balcom, V., Baltescu, P., Bao, H., Bavarian, M., Belgum, J., Bello, I., Berdine, J., Bernadett-Shapiro, G., Berner, C., Bogdonoff, L., Boiko, O., Boyd, M., Brakman, A.-L., Brockman, G., Brooks, T., Brundage, M., Button, K., Cai, T., Campbell, R., Cann, A., Carey, B., Carlson, C., Carmichael, R., Chan, B., Chang, C., Chantzis, F., Chen, D., Chen, S., Chen, R., Chen, J., Chen, M., Chess, B., Cho, C., Chu, C., Chung, H. W., Cummings, D., Currier, J., Dai, Y., Decareaux, C., Degry, T., Deutsch, N., Deville, D., Dhar, A., Dohan, D., Dowling, S., Dunning, S., Ecoffet, A., Eleti, A., Eloundou, T., Farhi, D., Fedus, L., Felix, N., Fishman, S. P., Forte, J., Fulford, I., Gao, L., Georges, E., Gibson, C., Goel, V., Gogineni, T., Goh, G., Gontijo-Lopes, R., Gordon, J., Grafstein, M., Gray, S., Greene, R., Gross, J., Gu, S. S., Guo, Y., Hallacy,
  C., Han, J., Harris, J., He, Y., Heaton, M., Heidecke, J., Hesse, C., Hickey, A., Hickey, W., Hoeschele, P., Houghton, B., Hsu, K., Hu, S., Hu, X., Huizinga, J., Jain, S., Jain, S., Jang, J., Jiang, A., Jiang, R., Jin, H., Jin, D., Jomoto, S., Jonn, B., Jun, H., Kaftan, T., Łukasz Kaiser, Kamali, A., Kanitscheider, I., Keskar, N. S., Khan, T., Kilpatrick, L., Kim, J. W., Kim, C., Kim, Y., Kirchner, J. H., Kiros, J., Knight, M., Kokotajlo, D., Łukasz Kondraciuk, Kondrich, A., Konstantinidis, A., Kosic, K., Krueger, G., Kuo, V., Lampe, M., Lan, I., Lee, T., Leike, J., Leung, J., Levy, D., Li, C. M., Lim, R., Lin, M., Lin, S., Litwin, M., Lopez, T., Lowe, R., Lue, P., Makanju, A., Malfacini, K., Manning, S., Markov, T., Markovski, Y., Martin, B., Mayer, K., Mayne, A., McGrew, B., McKinney, S. M., McLeavey, C., McMillan, P., McNeil, J., Medina, D., Mehta, A., Menick, J., Metz, L., Mishchenko, A., Mishkin, P., Monaco, V., Morikawa, E., Mossing, D., Mu, T., Murati, M., Murk, O., Mély, D., Nair, A., Nakano, R.,
  Nayak, R., Neelakantan, A., Ngo, R., Noh, H., Ouyang, L., O’Keefe, C., Pachocki, J., Paino, A., Palermo, J., Pantuliano, A., Parascandolo, G., Parish, J., Parparita, E., Passos, A., Pavlov, M., Peng, A., Perelman, A., de Avila Belbute Peres, F., Petrov, M., de Oliveira Pinto, H. P., Michael, Pokorny, Pokrass, M., Pong, V. H., Powell, T., Power, A., Power, B., Proehl, E., Puri, R., Radford, A., Rae, J., Ramesh, A., Raymond, C., Real, F., Rimbach, K., Ross, C., Rotsted, B., Roussez, H., Ryder, N., Saltarelli, M., Sanders, T., Santurkar, S., Sastry, G., Schmidt, H., Schnurr, D., Schulman, J., Selsam, D., Sheppard, K., Sherbakov, T., Shieh, J., Shoker, S., Shyam, P., Sidor, S., Sigler, E., Simens, M., Sitkin, J., Slama, K., Sohl, I., Sokolowsky, B., Song, Y., Staudacher, N., Such, F. P., Summers, N., Sutskever, I., Tang, J., Tezak, N., Thompson, M. B., Tillet, P., Tootoonchian, A., Tseng, E., Tuggle, P., Turley, N., Tworek, J., Uribe, J. F. C., Vallone, A., Vijayvergiya, A., Voss, C., Wainwright, C., Wang,
  J. J., Wang, A., Wang, B., Ward, J., Wei, J., Weinmann, C., Welihinda, A., Welinder, P., Weng, J., Weng, L., Wiethoff, M., Willner, D., Winter, C., Wolrich, S., Wong, H., Workman, L., Wu, S., Wu, J., Wu, M., Xiao, K., Xu, T., Yoo, S., Yu, K., Yuan, Q., Zaremba, W., Zellers, R., Zhang, C., Zhang, M., Zhao, S., Zheng, T., Zhuang, J., Zhuk, W., and Zoph, B.
  Gpt-4 technical report, 2024.
  URL <https://arxiv.org/abs/2303.08774>.
- Owen (2024)

  Owen, D.
  How predictable is language model benchmark performance?, 2024.
- Pachocki et al. (2024)

  Pachocki, J., Tworek, J., Fedus, L., Kaiser, L., Chen, M., Sidor, S., and Zaremba, W.
  Learning to reason with LLMs.
  Technical report, OpenAI, September 2024.
  URL <https://openai.com/index/learning-to-reason-with-llms>.
  Contributors include the o1 Contributions team, Core Contributors, and multiple research and safety teams.
- Paquette et al. (2024)

  Paquette, E., Paquette, C., Xiao, L., and Pennington, J.
  4+ 3 phases of compute-optimal neural scaling laws.
  *arXiv preprint arXiv:2405.15074*, 2024.
- Pinkus (1999)

  Pinkus, A.
  Approximation theory of the mlp model in neural networks.
  *Acta numerica*, 8:143–195, 1999.
- Polo et al. (2024)

  Polo, F. M., Somerstep, S., Choshen, L., Sun, Y., and Yurochkin, M.
  Sloth: scaling laws for llm skills to predict multi-benchmark performance across families, 2024.
  URL <https://arxiv.org/abs/2412.06540>.
- Porian et al. (2024)

  Porian, T., Wortsman, M., Jitsev, J., Schmidt, L., and Carmon, Y.
  Resolving discrepancies in compute-optimal scaling of language models, 2024.
  URL <https://arxiv.org/abs/2406.19146>.
- Reuel et al. (2024)

  Reuel, A., Bucknall, B., Casper, S., Fist, T., Soder, L., Aarne, O., Hammond, L., Ibrahim, L., Chan, A., Wills, P., Anderljung, M., Garfinkel, B., Heim, L., Trask, A., Mukobi, G., Schaeffer, R., Baker, M., Hooker, S., Solaiman, I., Luccioni, A. S., Rajkumar, N., Moës, N., Ladish, J., Guha, N., Newman, J., Bengio, Y., South, T., Pentland, A., Koyejo, S., Kochenderfer, M. J., and Trager, R.
  Open problems in technical ai governance, 2024.
  URL <https://arxiv.org/abs/2407.14981>.
- Roberts et al. (2022)

  Roberts, D. A., Yaida, S., and Hanin, B.
  *The principles of deep learning theory*, volume 46.
  Cambridge University Press Cambridge, MA, USA, 2022.
- Romani et al. (2013)

  Romani, S., Pinkoviezky, I., Rubin, A., and Tsodyks, M.
  Scaling laws of associative memory retrieval.
  *Neural computation*, 25(10):2523–2544, 2013.
- Rosenfeld et al. (2020)

  Rosenfeld, J. S., Rosenfeld, A., Belinkov, Y., and Shavit, N.
  A constructive prediction of the generalization error across scales.
  In *International Conference on Learning Representations*, 2020.
- Rosenfeld et al. (2021)

  Rosenfeld, J. S., Frankle, J., Carbin, M., and Shavit, N.
  On the predictability of pruning across scales.
  In Meila, M. and Zhang, T. (eds.), *Proceedings of the 38th International Conference on Machine Learning*, volume 139 of *Proceedings of Machine Learning Research*, pp. 9075–9083. PMLR, 18–24 Jul 2021.
  URL <https://proceedings.mlr.press/v139/rosenfeld21a.html>.
- Ruan et al. (2024)

  Ruan, Y., Maddison, C. J., and Hashimoto, T.
  Observational scaling laws and the predictability of language model performance, 2024.
  URL <https://arxiv.org/abs/2405.10938>.
- Sardana et al. (2023)

  Sardana, N., Portes, J., Doubov, S., and Frankle, J.
  Beyond chinchilla-optimal: Accounting for inference in language model scaling laws.
  In *Forty-first International Conference on Machine Learning*, 2023.
- Schaeffer (2023)

  Schaeffer, R.
  Pretraining on the test set is all you need, 2023.
  URL <https://arxiv.org/abs/2309.08632>.
- Schaeffer et al. (2023)

  Schaeffer, R., Miranda, B., and Koyejo, S.
  Are emergent abilities of large language models a mirage?
  In Oh, A., Naumann, T., Globerson, A., Saenko, K., Hardt, M., and Levine, S. (eds.), *Advances in Neural Information Processing Systems*, volume 36, pp. 55565–55581. Curran Associates, Inc., 2023.
  URL <https://proceedings.neurips.cc/paper_files/paper/2023/file/adc98a266f45005c403b8311ca7e8bd7-Paper-Conference.pdf>.
- Schaeffer et al. (2024a)

  Schaeffer, R., Lecomte, V., Pai, D. B., Carranza, A., Isik, B., Unell, A., Khona, M., Yerxa, T., LeCun, Y., Chung, S., Gromov, A., Shwartz-Ziv, R., and Koyejo, S.
  Towards an improved understanding and utilization of maximum manifold capacity representations, 2024a.
  URL <https://arxiv.org/abs/2406.09366>.
- Schaeffer et al. (2024b)

  Schaeffer, R., Schoelkopf, H., Miranda, B., Mukobi, G., Madan, V., Ibrahim, A., Bradley, H., Biderman, S., and Koyejo, S.
  Why has predicting downstream capabilities of frontier ai models with scale remained elusive?, 2024b.
  URL <https://arxiv.org/abs/2406.04391>.
- Schaeffer et al. (2024c)

  Schaeffer, R., Zahedi, N., Khona, M., Pai, D., Truong, S., Du, Y., Ostrow, M., Chandra, S., Carranza, A., Fiete, I. R., Gromov, A., and Koyejo, S.
  Bridging associative memory and probabilistic modeling, 2024c.
  URL <https://arxiv.org/abs/2402.10202>.
- Sharma & Kaplan (2022)

  Sharma, U. and Kaplan, J.
  Scaling laws from the data manifold dimension.
  *Journal of Machine Learning Research*, 23(9):1–34, 2022.
- Snell et al. (2024a)

  Snell, C., Lee, J., Xu, K., and Kumar, A.
  Scaling llm test-time compute optimally can be more effective than scaling model parameters.
  *arXiv preprint arXiv:2408.03314*, 2024a.
- Snell et al. (2024b)

  Snell, C., Wallace, E., Klein, D., and Levine, S.
  Predicting emergent capabilities by finetuning, 2024b.
  URL <https://arxiv.org/abs/2411.16035>.
- Sorscher et al. (2022)

  Sorscher, B., Geirhos, R., Shekhar, S., Ganguli, S., and Morcos, A.
  Beyond neural scaling laws: beating power law scaling via data pruning.
  *Advances in Neural Information Processing Systems*, 35:19523–19536, 2022.
- Spigler et al. (2020)

  Spigler, S., Geiger, M., and Wyart, M.
  Asymptotic learning curves of kernel methods: empirical data versus teacher–student paradigm.
  *Journal of Statistical Mechanics: Theory and Experiment*, 2020(12):124001, December 2020.
  ISSN 1742-5468.
  doi: 10.1088/1742-5468/abc61d.
  URL <http://dx.doi.org/10.1088/1742-5468/abc61d>.
- Srivastava et al. (2023)

  Srivastava, A., Rastogi, A., Rao, A., Shoeb, A. A. M., Abid, A., Fisch, A., Brown, A. R., Santoro, A., Gupta, A., Garriga-Alonso, A., Kluska, A., Lewkowycz, A., Agarwal, A., Power, A., Ray, A., Warstadt, A., Kocurek, A. W., Safaya, A., Tazarv, A., Xiang, A., Parrish, A., Nie, A., Hussain, A., Askell, A., Dsouza, A., Slone, A., Rahane, A., Iyer, A. S., Andreassen, A., Madotto, A., Santilli, A., Stuhlmüller, A., Dai, A., La, A., Lampinen, A., Zou, A., Jiang, A., Chen, A., Vuong, A., Gupta, A., Gottardi, A., Norelli, A., Venkatesh, A., Gholamidavoodi, A., Tabassum, A., Menezes, A., Kirubarajan, A., Mullokandov, A., Sabharwal, A., Herrick, A., Efrat, A., Erdem, A., Karakaş, A., Roberts, B. R., Loe, B. S., Zoph, B., Bojanowski, B., Özyurt, B., Hedayatnia, B., Neyshabur, B., Inden, B., Stein, B., Ekmekci, B., Lin, B. Y., Howald, B., Orinion, B., Diao, C., Dour, C., Stinson, C., Argueta, C., Ramírez, C. F., Singh, C., Rathkopf, C., Meng, C., Baral, C., Wu, C., Callison-Burch, C., Waites, C., Voigt, C., Manning,
  C. D., Potts, C., Ramirez, C., Rivera, C. E., Siro, C., Raffel, C., Ashcraft, C., Garbacea, C., Sileo, D., Garrette, D., Hendrycks, D., Kilman, D., Roth, D., Freeman, D., Khashabi, D., Levy, D., González, D. M., Perszyk, D., Hernandez, D., Chen, D., Ippolito, D., Gilboa, D., Dohan, D., Drakard, D., Jurgens, D., Datta, D., Ganguli, D., Emelin, D., Kleyko, D., Yuret, D., Chen, D., Tam, D., Hupkes, D., Misra, D., Buzan, D., Mollo, D. C., Yang, D., Lee, D.-H., Schrader, D., Shutova, E., Cubuk, E. D., Segal, E., Hagerman, E., Barnes, E., Donoway, E., Pavlick, E., Rodola, E., Lam, E., Chu, E., Tang, E., Erdem, E., Chang, E., Chi, E. A., Dyer, E., Jerzak, E., Kim, E., Manyasi, E. E., Zheltonozhskii, E., Xia, F., Siar, F., Martínez-Plumed, F., Happé, F., Chollet, F., Rong, F., Mishra, G., Winata, G. I., de Melo, G., Kruszewski, G., Parascandolo, G., Mariani, G., Wang, G., Jaimovitch-López, G., Betz, G., Gur-Ari, G., Galijasevic, H., Kim, H., Rashkin, H., Hajishirzi, H., Mehta, H., Bogar, H., Shevlin, H.,
  Schütze, H., Yakura, H., Zhang, H., Wong, H. M., Ng, I., Noble, I., Jumelet, J., Geissinger, J., Kernion, J., Hilton, J., Lee, J., Fisac, J. F., Simon, J. B., Koppel, J., Zheng, J., Zou, J., Kocoń, J., Thompson, J., Wingfield, J., Kaplan, J., Radom, J., Sohl-Dickstein, J., Phang, J., Wei, J., Yosinski, J., Novikova, J., Bosscher, J., Marsh, J., Kim, J., Taal, J., Engel, J., Alabi, J., Xu, J., Song, J., Tang, J., Waweru, J., Burden, J., Miller, J., Balis, J. U., Batchelder, J., Berant, J., Frohberg, J., Rozen, J., Hernandez-Orallo, J., Boudeman, J., Guerr, J., Jones, J., Tenenbaum, J. B., Rule, J. S., Chua, J., Kanclerz, K., Livescu, K., Krauth, K., Gopalakrishnan, K., Ignatyeva, K., Markert, K., Dhole, K. D., Gimpel, K., Omondi, K., Mathewson, K., Chiafullo, K., Shkaruta, K., Shridhar, K., McDonell, K., Richardson, K., Reynolds, L., Gao, L., Zhang, L., Dugan, L., Qin, L., Contreras-Ochando, L., Morency, L.-P., Moschella, L., Lam, L., Noble, L., Schmidt, L., He, L., Colón, L. O., Metz, L., Şenel, L. K.,
  Bosma, M., Sap, M., ter Hoeve, M., Farooqi, M., Faruqui, M., Mazeika, M., Baturan, M., Marelli, M., Maru, M., Quintana, M. J. R., Tolkiehn, M., Giulianelli, M., Lewis, M., Potthast, M., Leavitt, M. L., Hagen, M., Schubert, M., Baitemirova, M. O., Arnaud, M., McElrath, M., Yee, M. A., Cohen, M., Gu, M., Ivanitskiy, M., Starritt, M., Strube, M., Swędrowski, M., Bevilacqua, M., Yasunaga, M., Kale, M., Cain, M., Xu, M., Suzgun, M., Walker, M., Tiwari, M., Bansal, M., Aminnaseri, M., Geva, M., Gheini, M., T, M. V., Peng, N., Chi, N. A., Lee, N., Krakover, N. G.-A., Cameron, N., Roberts, N., Doiron, N., Martinez, N., Nangia, N., Deckers, N., Muennighoff, N., Keskar, N. S., Iyer, N. S., Constant, N., Fiedel, N., Wen, N., Zhang, O., Agha, O., Elbaghdadi, O., Levy, O., Evans, O., Casares, P. A. M., Doshi, P., Fung, P., Liang, P. P., Vicol, P., Alipoormolabashi, P., Liao, P., Liang, P., Chang, P., Eckersley, P., Htut, P. M., Hwang, P., Miłkowski, P., Patil, P., Pezeshkpour, P., Oli, P., Mei, Q., Lyu, Q., Chen, Q.,
  Banjade, R., Rudolph, R. E., Gabriel, R., Habacker, R., Risco, R., Millière, R., Garg, R., Barnes, R., Saurous, R. A., Arakawa, R., Raymaekers, R., Frank, R., Sikand, R., Novak, R., Sitelew, R., LeBras, R., Liu, R., Jacobs, R., Zhang, R., Salakhutdinov, R., Chi, R., Lee, R., Stovall, R., Teehan, R., Yang, R., Singh, S., Mohammad, S. M., Anand, S., Dillavou, S., Shleifer, S., Wiseman, S., Gruetter, S., Bowman, S. R., Schoenholz, S. S., Han, S., Kwatra, S., Rous, S. A., Ghazarian, S., Ghosh, S., Casey, S., Bischoff, S., Gehrmann, S., Schuster, S., Sadeghi, S., Hamdan, S., Zhou, S., Srivastava, S., Shi, S., Singh, S., Asaadi, S., Gu, S. S., Pachchigar, S., Toshniwal, S., Upadhyay, S., Shyamolima, Debnath, Shakeri, S., Thormeyer, S., Melzi, S., Reddy, S., Makini, S. P., Lee, S.-H., Torene, S., Hatwar, S., Dehaene, S., Divic, S., Ermon, S., Biderman, S., Lin, S., Prasad, S., Piantadosi, S. T., Shieber, S. M., Misherghi, S., Kiritchenko, S., Mishra, S., Linzen, T., Schuster, T., Li, T., Yu, T., Ali, T.,
  Hashimoto, T., Wu, T.-L., Desbordes, T., Rothschild, T., Phan, T., Wang, T., Nkinyili, T., Schick, T., Kornev, T., Tunduny, T., Gerstenberg, T., Chang, T., Neeraj, T., Khot, T., Shultz, T., Shaham, U., Misra, V., Demberg, V., Nyamai, V., Raunak, V., Ramasesh, V., Prabhu, V. U., Padmakumar, V., Srikumar, V., Fedus, W., Saunders, W., Zhang, W., Vossen, W., Ren, X., Tong, X., Zhao, X., Wu, X., Shen, X., Yaghoobzadeh, Y., Lakretz, Y., Song, Y., Bahri, Y., Choi, Y., Yang, Y., Hao, Y., Chen, Y., Belinkov, Y., Hou, Y., Hou, Y., Bai, Y., Seid, Z., Zhao, Z., Wang, Z., Wang, Z. J., Wang, Z., and Wu, Z.
  Beyond the imitation game: Quantifying and extrapolating the capabilities of language models, 2023.
  URL <https://arxiv.org/abs/2206.04615>.
- Sun et al. (2025)

  Sun, X., Li, S., Xie, R., Han, W., Wu, K., Yang, Z., Li, Y., Wang, A., Li, S., Xue, J., Cheng, Y., Tao, Y., Kang, Z., Xu, C., Wang, D., and Jiang, J.
  Scaling laws for floating point quantization training, 2025.
  URL <https://arxiv.org/abs/2501.02423>.
- Tao et al. (2024)

  Tao, C., Liu, Q., Dou, L., Muennighoff, N., Wan, Z., Luo, P., Lin, M., and Wong, N.
  Scaling laws with vocabulary: Larger models deserve larger vocabularies.
  *arXiv preprint arXiv:2407.13623*, 2024.
- Tay et al. (2021)

  Tay, Y., Dehghani, M., Rao, J., Fedus, W., Abnar, S., Chung, H. W., Narang, S., Yogatama, D., Vaswani, A., and Metzler, D.
  Scale efficiently: Insights from pre-training and fine-tuning transformers.
  *arXiv preprint arXiv:2109.10686*, 2021.
- Tay et al. (2022a)

  Tay, Y., Dehghani, M., Abnar, S., Chung, H. W., Fedus, W., Rao, J., Narang, S., Tran, V. Q., Yogatama, D., and Metzler, D.
  Scaling laws vs model architectures: How does inductive bias influence scaling?
  In *The 2023 Conference on Empirical Methods in Natural Language Processing*, 2022a.
- Tay et al. (2022b)

  Tay, Y., Wei, J., Chung, H. W., Tran, V. Q., So, D. R., Shakeri, S., Garcia, X., Zheng, H. S., Rao, J., Chowdhery, A., Zhou, D., Metzler, D., Petrov, S., Houlsby, N., Le, Q. V., and Dehghani, M.
  Transcending scaling laws with 0.1
  URL <https://arxiv.org/abs/2210.11399>.
- Team et al. (2024a)

  Team, G., Anil, R., Borgeaud, S., Alayrac, J.-B., Yu, J., Soricut, R., Schalkwyk, J., Dai, A. M., Hauth, A., Millican, K., Silver, D., Johnson, M., Antonoglou, I., Schrittwieser, J., Glaese, A., Chen, J., Pitler, E., Lillicrap, T., Lazaridou, A., Firat, O., Molloy, J., Isard, M., Barham, P. R., Hennigan, T., Lee, B., Viola, F., Reynolds, M., Xu, Y., Doherty, R., Collins, E., Meyer, C., Rutherford, E., Moreira, E., Ayoub, K., Goel, M., Krawczyk, J., Du, C., Chi, E., Cheng, H.-T., Ni, E., Shah, P., Kane, P., Chan, B., Faruqui, M., Severyn, A., Lin, H., Li, Y., Cheng, Y., Ittycheriah, A., Mahdieh, M., Chen, M., Sun, P., Tran, D., Bagri, S., Lakshminarayanan, B., Liu, J., Orban, A., Güra, F., Zhou, H., Song, X., Boffy, A., Ganapathy, H., Zheng, S., Choe, H., Ágoston Weisz, Zhu, T., Lu, Y., Gopal, S., Kahn, J., Kula, M., Pitman, J., Shah, R., Taropa, E., Merey, M. A., Baeuml, M., Chen, Z., Shafey, L. E., Zhang, Y., Sercinoglu, O., Tucker, G., Piqueras, E., Krikun, M., Barr, I., Savinov, N., Danihelka, I.,
  Roelofs, B., White, A., Andreassen, A., von Glehn, T., Yagati, L., Kazemi, M., Gonzalez, L., Khalman, M., Sygnowski, J., Frechette, A., Smith, C., Culp, L., Proleev, L., Luan, Y., Chen, X., Lottes, J., Schucher, N., Lebron, F., Rrustemi, A., Clay, N., Crone, P., Kocisky, T., Zhao, J., Perz, B., Yu, D., Howard, H., Bloniarz, A., Rae, J. W., Lu, H., Sifre, L., Maggioni, M., Alcober, F., Garrette, D., Barnes, M., Thakoor, S., Austin, J., Barth-Maron, G., Wong, W., Joshi, R., Chaabouni, R., Fatiha, D., Ahuja, A., Tomar, G. S., Senter, E., Chadwick, M., Kornakov, I., Attaluri, N., Iturrate, I., Liu, R., Li, Y., Cogan, S., Chen, J., Jia, C., Gu, C., Zhang, Q., Grimstad, J., Hartman, A. J., Garcia, X., Pillai, T. S., Devlin, J., Laskin, M., de Las Casas, D., Valter, D., Tao, C., Blanco, L., Badia, A. P., Reitter, D., Chen, M., Brennan, J., Rivera, C., Brin, S., Iqbal, S., Surita, G., Labanowski, J., Rao, A., Winkler, S., Parisotto, E., Gu, Y., Olszewska, K., Addanki, R., Miech, A., Louis, A., Teplyashin, D.,
  Brown, G., Catt, E., Balaguer, J., Xiang, J., Wang, P., Ashwood, Z., Briukhov, A., Webson, A., Ganapathy, S., Sanghavi, S., Kannan, A., Chang, M.-W., Stjerngren, A., Djolonga, J., Sun, Y., Bapna, A., Aitchison, M., Pejman, P., Michalewski, H., Yu, T., Wang, C., Love, J., Ahn, J., Bloxwich, D., Han, K., Humphreys, P., Sellam, T., Bradbury, J., Godbole, V., Samangooei, S., Damoc, B., Kaskasoli, A., Arnold, S. M. R., Vasudevan, V., Agrawal, S., Riesa, J., Lepikhin, D., Tanburn, R., Srinivasan, S., Lim, H., Hodkinson, S., Shyam, P., Ferret, J., Hand, S., Garg, A., Paine, T. L., Li, J., Li, Y., Giang, M., Neitz, A., Abbas, Z., York, S., Reid, M., Cole, E., Chowdhery, A., Das, D., Rogozińska, D., Nikolaev, V., Sprechmann, P., Nado, Z., Zilka, L., Prost, F., He, L., Monteiro, M., Mishra, G., Welty, C., Newlan, J., Jia, D., Allamanis, M., Hu, C. H., de Liedekerke, R., Gilmer, J., Saroufim, C., Rijhwani, S., Hou, S., Shrivastava, D., Baddepudi, A., Goldin, A., Ozturel, A., Cassirer, A., Xu, Y., Sohn, D., Sachan,
  D., Amplayo, R. K., Swanson, C., Petrova, D., Narayan, S., Guez, A., Brahma, S., Landon, J., Patel, M., Zhao, R., Villela, K., Wang, L., Jia, W., Rahtz, M., Giménez, M., Yeung, L., Keeling, J., Georgiev, P., Mincu, D., Wu, B., Haykal, S., Saputro, R., Vodrahalli, K., Qin, J., Cankara, Z., Sharma, A., Fernando, N., Hawkins, W., Neyshabur, B., Kim, S., Hutter, A., Agrawal, P., Castro-Ros, A., van den Driessche, G., Wang, T., Yang, F., yiin Chang, S., Komarek, P., McIlroy, R., Lučić, M., Zhang, G., Farhan, W., Sharman, M., Natsev, P., Michel, P., Bansal, Y., Qiao, S., Cao, K., Shakeri, S., Butterfield, C., Chung, J., Rubenstein, P. K., Agrawal, S., Mensch, A., Soparkar, K., Lenc, K., Chung, T., Pope, A., Maggiore, L., Kay, J., Jhakra, P., Wang, S., Maynez, J., Phuong, M., Tobin, T., Tacchetti, A., Trebacz, M., Robinson, K., Katariya, Y., Riedel, S., Bailey, P., Xiao, K., Ghelani, N., Aroyo, L., Slone, A., Houlsby, N., Xiong, X., Yang, Z., Gribovskaya, E., Adler, J., Wirth, M., Lee, L., Li, M., Kagohara, T.,
  Pavagadhi, J., Bridgers, S., Bortsova, A., Ghemawat, S., Ahmed, Z., Liu, T., Powell, R., Bolina, V., Iinuma, M., Zablotskaia, P., Besley, J., Chung, D.-W., Dozat, T., Comanescu, R., Si, X., Greer, J., Su, G., Polacek, M., Kaufman, R. L., Tokumine, S., Hu, H., Buchatskaya, E., Miao, Y., Elhawaty, M., Siddhant, A., Tomasev, N., Xing, J., Greer, C., Miller, H., Ashraf, S., Roy, A., Zhang, Z., Ma, A., Filos, A., Besta, M., Blevins, R., Klimenko, T., Yeh, C.-K., Changpinyo, S., Mu, J., Chang, O., Pajarskas, M., Muir, C., Cohen, V., Lan, C. L., Haridasan, K., Marathe, A., Hansen, S., Douglas, S., Samuel, R., Wang, M., Austin, S., Lan, C., Jiang, J., Chiu, J., Lorenzo, J. A., Sjösund, L. L., Cevey, S., Gleicher, Z., Avrahami, T., Boral, A., Srinivasan, H., Selo, V., May, R., Aisopos, K., Hussenot, L., Soares, L. B., Baumli, K., Chang, M. B., Recasens, A., Caine, B., Pritzel, A., Pavetic, F., Pardo, F., Gergely, A., Frye, J., Ramasesh, V., Horgan, D., Badola, K., Kassner, N., Roy, S., Dyer, E., Campos, V. C.,
  Tomala, A., Tang, Y., Badawy, D. E., White, E., Mustafa, B., Lang, O., Jindal, A., Vikram, S., Gong, Z., Caelles, S., Hemsley, R., Thornton, G., Feng, F., Stokowiec, W., Zheng, C., Thacker, P., Çağlar Ünlü, Zhang, Z., Saleh, M., Svensson, J., Bileschi, M., Patil, P., Anand, A., Ring, R., Tsihlas, K., Vezer, A., Selvi, M., Shevlane, T., Rodriguez, M., Kwiatkowski, T., Daruki, S., Rong, K., Dafoe, A., FitzGerald, N., Gu-Lemberg, K., Khan, M., Hendricks, L. A., Pellat, M., Feinberg, V., Cobon-Kerr, J., Sainath, T., Rauh, M., Hashemi, S. H., Ives, R., Hasson, Y., Noland, E., Cao, Y., Byrd, N., Hou, L., Wang, Q., Sottiaux, T., Paganini, M., Lespiau, J.-B., Moufarek, A., Hassan, S., Shivakumar, K., van Amersfoort, J., Mandhane, A., Joshi, P., Goyal, A., Tung, M., Brock, A., Sheahan, H., Misra, V., Li, C., Rakićević, N., Dehghani, M., Liu, F., Mittal, S., Oh, J., Noury, S., Sezener, E., Huot, F., Lamm, M., Cao, N. D., Chen, C., Mudgal, S., Stella, R., Brooks, K., Vasudevan, G., Liu, C., Chain, M., Melinkeri,
  N., Cohen, A., Wang, V., Seymore, K., Zubkov, S., Goel, R., Yue, S., Krishnakumaran, S., Albert, B., Hurley, N., Sano, M., Mohananey, A., Joughin, J., Filonov, E., Kepa, T., Eldawy, Y., Lim, J., Rishi, R., Badiezadegan, S., Bos, T., Chang, J., Jain, S., Padmanabhan, S. G. S., Puttagunta, S., Krishna, K., Baker, L., Kalb, N., Bedapudi, V., Kurzrok, A., Lei, S., Yu, A., Litvin, O., Zhou, X., Wu, Z., Sobell, S., Siciliano, A., Papir, A., Neale, R., Bragagnolo, J., Toor, T., Chen, T., Anklin, V., Wang, F., Feng, R., Gholami, M., Ling, K., Liu, L., Walter, J., Moghaddam, H., Kishore, A., Adamek, J., Mercado, T., Mallinson, J., Wandekar, S., Cagle, S., Ofek, E., Garrido, G., Lombriser, C., Mukha, M., Sun, B., Mohammad, H. R., Matak, J., Qian, Y., Peswani, V., Janus, P., Yuan, Q., Schelin, L., David, O., Garg, A., He, Y., Duzhyi, O., Älgmyr, A., Lottaz, T., Li, Q., Yadav, V., Xu, L., Chinien, A., Shivanna, R., Chuklin, A., Li, J., Spadine, C., Wolfe, T., Mohamed, K., Das, S., Dai, Z., He, K., von Dincklage, D.,
  Upadhyay, S., Maurya, A., Chi, L., Krause, S., Salama, K., Rabinovitch, P. G., M, P. K. R., Selvan, A., Dektiarev, M., Ghiasi, G., Guven, E., Gupta, H., Liu, B., Sharma, D., Shtacher, I. H., Paul, S., Akerlund, O., Aubet, F.-X., Huang, T., Zhu, C., Zhu, E., Teixeira, E., Fritze, M., Bertolini, F., Marinescu, L.-E., Bölle, M., Paulus, D., Gupta, K., Latkar, T., Chang, M., Sanders, J., Wilson, R., Wu, X., Tan, Y.-X., Thiet, L. N., Doshi, T., Lall, S., Mishra, S., Chen, W., Luong, T., Benjamin, S., Lee, J., Andrejczuk, E., Rabiej, D., Ranjan, V., Styrc, K., Yin, P., Simon, J., Harriott, M. R., Bansal, M., Robsky, A., Bacon, G., Greene, D., Mirylenka, D., Zhou, C., Sarvana, O., Goyal, A., Andermatt, S., Siegler, P., Horn, B., Israel, A., Pongetti, F., Chen, C.-W. L., Selvatici, M., Silva, P., Wang, K., Tolins, J., Guu, K., Yogev, R., Cai, X., Agostini, A., Shah, M., Nguyen, H., Donnaile, N. O., Pereira, S., Friso, L., Stambler, A., Kurzrok, A., Kuang, C., Romanikhin, Y., Geller, M., Yan, Z., Jang, K., Lee,
  C.-C., Fica, W., Malmi, E., Tan, Q., Banica, D., Balle, D., Pham, R., Huang, Y., Avram, D., Shi, H., Singh, J., Hidey, C., Ahuja, N., Saxena, P., Dooley, D., Potharaju, S. P., O’Neill, E., Gokulchandran, A., Foley, R., Zhao, K., Dusenberry, M., Liu, Y., Mehta, P., Kotikalapudi, R., Safranek-Shrader, C., Goodman, A., Kessinger, J., Globen, E., Kolhar, P., Gorgolewski, C., Ibrahim, A., Song, Y., Eichenbaum, A., Brovelli, T., Potluri, S., Lahoti, P., Baetu, C., Ghorbani, A., Chen, C., Crawford, A., Pal, S., Sridhar, M., Gurita, P., Mujika, A., Petrovski, I., Cedoz, P.-L., Li, C., Chen, S., Santo, N. D., Goyal, S., Punjabi, J., Kappaganthu, K., Kwak, C., LV, P., Velury, S., Choudhury, H., Hall, J., Shah, P., Figueira, R., Thomas, M., Lu, M., Zhou, T., Kumar, C., Jurdi, T., Chikkerur, S., Ma, Y., Yu, A., Kwak, S., Ähdel, V., Rajayogam, S., Choma, T., Liu, F., Barua, A., Ji, C., Park, J. H., Hellendoorn, V., Bailey, A., Bilal, T., Zhou, H., Khatir, M., Sutton, C., Rzadkowski, W., Macintosh, F., Shagin, K.,
  Medina, P., Liang, C., Zhou, J., Shah, P., Bi, Y., Dankovics, A., Banga, S., Lehmann, S., Bredesen, M., Lin, Z., Hoffmann, J. E., Lai, J., Chung, R., Yang, K., Balani, N., Bražinskas, A., Sozanschi, A., Hayes, M., Alcalde, H. F., Makarov, P., Chen, W., Stella, A., Snijders, L., Mandl, M., Kärrman, A., Nowak, P., Wu, X., Dyck, A., Vaidyanathan, K., R, R., Mallet, J., Rudominer, M., Johnston, E., Mittal, S., Udathu, A., Christensen, J., Verma, V., Irving, Z., Santucci, A., Elsayed, G., Davoodi, E., Georgiev, M., Tenney, I., Hua, N., Cideron, G., Leurent, E., Alnahlawi, M., Georgescu, I., Wei, N., Zheng, I., Scandinaro, D., Jiang, H., Snoek, J., Sundararajan, M., Wang, X., Ontiveros, Z., Karo, I., Cole, J., Rajashekhar, V., Tumeh, L., Ben-David, E., Jain, R., Uesato, J., Datta, R., Bunyan, O., Wu, S., Zhang, J., Stanczyk, P., Zhang, Y., Steiner, D., Naskar, S., Azzam, M., Johnson, M., Paszke, A., Chiu, C.-C., Elias, J. S., Mohiuddin, A., Muhammad, F., Miao, J., Lee, A., Vieillard, N., Park, J., Zhang, J.,
  Stanway, J., Garmon, D., Karmarkar, A., Dong, Z., Lee, J., Kumar, A., Zhou, L., Evens, J., Isaac, W., Irving, G., Loper, E., Fink, M., Arkatkar, I., Chen, N., Shafran, I., Petrychenko, I., Chen, Z., Jia, J., Levskaya, A., Zhu, Z., Grabowski, P., Mao, Y., Magni, A., Yao, K., Snaider, J., Casagrande, N., Palmer, E., Suganthan, P., Castaño, A., Giannoumis, I., Kim, W., Rybiński, M., Sreevatsa, A., Prendki, J., Soergel, D., Goedeckemeyer, A., Gierke, W., Jafari, M., Gaba, M., Wiesner, J., Wright, D. G., Wei, Y., Vashisht, H., Kulizhskaya, Y., Hoover, J., Le, M., Li, L., Iwuanyanwu, C., Liu, L., Ramirez, K., Khorlin, A., Cui, A., LIN, T., Wu, M., Aguilar, R., Pallo, K., Chakladar, A., Perng, G., Abellan, E. A., Zhang, M., Dasgupta, I., Kushman, N., Penchev, I., Repina, A., Wu, X., van der Weide, T., Ponnapalli, P., Kaplan, C., Simsa, J., Li, S., Dousse, O., Yang, F., Piper, J., Ie, N., Pasumarthi, R., Lintz, N., Vijayakumar, A., Andor, D., Valenzuela, P., Lui, M., Paduraru, C., Peng, D., Lee, K., Zhang, S.,
  Greene, S., Nguyen, D. D., Kurylowicz, P., Hardin, C., Dixon, L., Janzer, L., Choo, K., Feng, Z., Zhang, B., Singhal, A., Du, D., McKinnon, D., Antropova, N., Bolukbasi, T., Keller, O., Reid, D., Finchelstein, D., Raad, M. A., Crocker, R., Hawkins, P., Dadashi, R., Gaffney, C., Franko, K., Bulanova, A., Leblond, R., Chung, S., Askham, H., Cobo, L. C., Xu, K., Fischer, F., Xu, J., Sorokin, C., Alberti, C., Lin, C.-C., Evans, C., Dimitriev, A., Forbes, H., Banarse, D., Tung, Z., Omernick, M., Bishop, C., Sterneck, R., Jain, R., Xia, J., Amid, E., Piccinno, F., Wang, X., Banzal, P., Mankowitz, D. J., Polozov, A., Krakovna, V., Brown, S., Bateni, M., Duan, D., Firoiu, V., Thotakuri, M., Natan, T., Geist, M., tan Girgin, S., Li, H., Ye, J., Roval, O., Tojo, R., Kwong, M., Lee-Thorp, J., Yew, C., Sinopalnikov, D., Ramos, S., Mellor, J., Sharma, A., Wu, K., Miller, D., Sonnerat, N., Vnukov, D., Greig, R., Beattie, J., Caveness, E., Bai, L., Eisenschlos, J., Korchemniy, A., Tsai, T., Jasarevic, M., Kong, W., Dao,
  P., Zheng, Z., Liu, F., Yang, F., Zhu, R., Teh, T. H., Sanmiya, J., Gladchenko, E., Trdin, N., Toyama, D., Rosen, E., Tavakkol, S., Xue, L., Elkind, C., Woodman, O., Carpenter, J., Papamakarios, G., Kemp, R., Kafle, S., Grunina, T., Sinha, R., Talbert, A., Wu, D., Owusu-Afriyie, D., Du, C., Thornton, C., Pont-Tuset, J., Narayana, P., Li, J., Fatehi, S., Wieting, J., Ajmeri, O., Uria, B., Ko, Y., Knight, L., Héliou, A., Niu, N., Gu, S., Pang, C., Li, Y., Levine, N., Stolovich, A., Santamaria-Fernandez, R., Goenka, S., Yustalim, W., Strudel, R., Elqursh, A., Deck, C., Lee, H., Li, Z., Levin, K., Hoffmann, R., Holtmann-Rice, D., Bachem, O., Arora, S., Koh, C., Yeganeh, S. H., Põder, S., Tariq, M., Sun, Y., Ionita, L., Seyedhosseini, M., Tafti, P., Liu, Z., Gulati, A., Liu, J., Ye, X., Chrzaszcz, B., Wang, L., Sethi, N., Li, T., Brown, B., Singh, S., Fan, W., Parisi, A., Stanton, J., Koverkathu, V., Choquette-Choo, C. A., Li, Y., Lu, T., Ittycheriah, A., Shroff, P., Varadarajan, M., Bahargam, S., Willoughby,
  R., Gaddy, D., Desjardins, G., Cornero, M., Robenek, B., Mittal, B., Albrecht, B., Shenoy, A., Moiseev, F., Jacobsson, H., Ghaffarkhah, A., Rivière, M., Walton, A., Crepy, C., Parrish, A., Zhou, Z., Farabet, C., Radebaugh, C., Srinivasan, P., van der Salm, C., Fidjeland, A., Scellato, S., Latorre-Chimoto, E., Klimczak-Plucińska, H., Bridson, D., de Cesare, D., Hudson, T., Mendolicchio, P., Walker, L., Morris, A., Mauger, M., Guseynov, A., Reid, A., Odoom, S., Loher, L., Cotruta, V., Yenugula, M., Grewe, D., Petrushkina, A., Duerig, T., Sanchez, A., Yadlowsky, S., Shen, A., Globerson, A., Webb, L., Dua, S., Li, D., Bhupatiraju, S., Hurt, D., Qureshi, H., Agarwal, A., Shani, T., Eyal, M., Khare, A., Belle, S. R., Wang, L., Tekur, C., Kale, M. S., Wei, J., Sang, R., Saeta, B., Liechty, T., Sun, Y., Zhao, Y., Lee, S., Nayak, P., Fritz, D., Vuyyuru, M. R., Aslanides, J., Vyas, N., Wicke, M., Ma, X., Eltyshev, E., Martin, N., Cate, H., Manyika, J., Amiri, K., Kim, Y., Xiong, X., Kang, K., Luisier, F.,
  Tripuraneni, N., Madras, D., Guo, M., Waters, A., Wang, O., Ainslie, J., Baldridge, J., Zhang, H., Pruthi, G., Bauer, J., Yang, F., Mansour, R., Gelman, J., Xu, Y., Polovets, G., Liu, J., Cai, H., Chen, W., Sheng, X., Xue, E., Ozair, S., Angermueller, C., Li, X., Sinha, A., Wang, W., Wiesinger, J., Koukoumidis, E., Tian, Y., Iyer, A., Gurumurthy, M., Goldenson, M., Shah, P., Blake, M., Yu, H., Urbanowicz, A., Palomaki, J., Fernando, C., Durden, K., Mehta, H., Momchev, N., Rahimtoroghi, E., Georgaki, M., Raul, A., Ruder, S., Redshaw, M., Lee, J., Zhou, D., Jalan, K., Li, D., Hechtman, B., Schuh, P., Nasr, M., Milan, K., Mikulik, V., Franco, J., Green, T., Nguyen, N., Kelley, J., Mahendru, A., Hu, A., Howland, J., Vargas, B., Hui, J., Bansal, K., Rao, V., Ghiya, R., Wang, E., Ye, K., Sarr, J. M., Preston, M. M., Elish, M., Li, S., Kaku, A., Gupta, J., Pasupat, I., Juan, D.-C., Someswar, M., M., T., Chen, X., Amini, A., Fabrikant, A., Chu, E., Dong, X., Muthal, A., Buthpitiya, S., Jauhari, S., Hua, N.,
  Khandelwal, U., Hitron, A., Ren, J., Rinaldi, L., Drath, S., Dabush, A., Jiang, N.-J., Godhia, H., Sachs, U., Chen, A., Fan, Y., Taitelbaum, H., Noga, H., Dai, Z., Wang, J., Liang, C., Hamer, J., Ferng, C.-S., Elkind, C., Atias, A., Lee, P., Listík, V., Carlen, M., van de Kerkhof, J., Pikus, M., Zaher, K., Müller, P., Zykova, S., Stefanec, R., Gatsko, V., Hirnschall, C., Sethi, A., Xu, X. F., Ahuja, C., Tsai, B., Stefanoiu, A., Feng, B., Dhandhania, K., Katyal, M., Gupta, A., Parulekar, A., Pitta, D., Zhao, J., Bhatia, V., Bhavnani, Y., Alhadlaq, O., Li, X., Danenberg, P., Tu, D., Pine, A., Filippova, V., Ghosh, A., Limonchik, B., Urala, B., Lanka, C. K., Clive, D., Sun, Y., Li, E., Wu, H., Hongtongsak, K., Li, I., Thakkar, K., Omarov, K., Majmundar, K., Alverson, M., Kucharski, M., Patel, M., Jain, M., Zabelin, M., Pelagatti, P., Kohli, R., Kumar, S., Kim, J., Sankar, S., Shah, V., Ramachandruni, L., Zeng, X., Bariach, B., Weidinger, L., Vu, T., Andreev, A., He, A., Hui, K., Kashem, S., Subramanya, A.,
  Hsiao, S., Hassabis, D., Kavukcuoglu, K., Sadovsky, A., Le, Q., Strohman, T., Wu, Y., Petrov, S., Dean, J., and Vinyals, O.
  Gemini: A family of highly capable multimodal models, 2024a.
  URL <https://arxiv.org/abs/2312.11805>.
- Team et al. (2024b)

  Team, G., Georgiev, P., Lei, V. I., Burnell, R., Bai, L., Gulati, A., Tanzer, G., Vincent, D., Pan, Z., Wang, S., Mariooryad, S., Ding, Y., Geng, X., Alcober, F., Frostig, R., Omernick, M., Walker, L., Paduraru, C., Sorokin, C., Tacchetti, A., Gaffney, C., Daruki, S., Sercinoglu, O., Gleicher, Z., Love, J., Voigtlaender, P., Jain, R., Surita, G., Mohamed, K., Blevins, R., Ahn, J., Zhu, T., Kawintiranon, K., Firat, O., Gu, Y., Zhang, Y., Rahtz, M., Faruqui, M., Clay, N., Gilmer, J., Co-Reyes, J., Penchev, I., Zhu, R., Morioka, N., Hui, K., Haridasan, K., Campos, V., Mahdieh, M., Guo, M., Hassan, S., Kilgour, K., Vezer, A., Cheng, H.-T., de Liedekerke, R., Goyal, S., Barham, P., Strouse, D., Noury, S., Adler, J., Sundararajan, M., Vikram, S., Lepikhin, D., Paganini, M., Garcia, X., Yang, F., Valter, D., Trebacz, M., Vodrahalli, K., Asawaroengchai, C., Ring, R., Kalb, N., Soares, L. B., Brahma, S., Steiner, D., Yu, T., Mentzer, F., He, A., Gonzalez, L., Xu, B., Kaufman, R. L., Shafey, L. E., Oh, J., Hennigan,
  T., van den Driessche, G., Odoom, S., Lucic, M., Roelofs, B., Lall, S., Marathe, A., Chan, B., Ontanon, S., He, L., Teplyashin, D., Lai, J., Crone, P., Damoc, B., Ho, L., Riedel, S., Lenc, K., Yeh, C.-K., Chowdhery, A., Xu, Y., Kazemi, M., Amid, E., Petrushkina, A., Swersky, K., Khodaei, A., Chen, G., Larkin, C., Pinto, M., Yan, G., Badia, A. P., Patil, P., Hansen, S., Orr, D., Arnold, S. M. R., Grimstad, J., Dai, A., Douglas, S., Sinha, R., Yadav, V., Chen, X., Gribovskaya, E., Austin, J., Zhao, J., Patel, K., Komarek, P., Austin, S., Borgeaud, S., Friso, L., Goyal, A., Caine, B., Cao, K., Chung, D.-W., Lamm, M., Barth-Maron, G., Kagohara, T., Olszewska, K., Chen, M., Shivakumar, K., Agarwal, R., Godhia, H., Rajwar, R., Snaider, J., Dotiwalla, X., Liu, Y., Barua, A., Ungureanu, V., Zhang, Y., Batsaikhan, B.-O., Wirth, M., Qin, J., Danihelka, I., Doshi, T., Chadwick, M., Chen, J., Jain, S., Le, Q., Kar, A., Gurumurthy, M., Li, C., Sang, R., Liu, F., Lamprou, L., Munoz, R., Lintz, N., Mehta, H., Howard, H.,
  Reynolds, M., Aroyo, L., Wang, Q., Blanco, L., Cassirer, A., Griffith, J., Das, D., Lee, S., Sygnowski, J., Fisher, Z., Besley, J., Powell, R., Ahmed, Z., Paulus, D., Reitter, D., Borsos, Z., Joshi, R., Pope, A., Hand, S., Selo, V., Jain, V., Sethi, N., Goel, M., Makino, T., May, R., Yang, Z., Schalkwyk, J., Butterfield, C., Hauth, A., Goldin, A., Hawkins, W., Senter, E., Brin, S., Woodman, O., Ritter, M., Noland, E., Giang, M., Bolina, V., Lee, L., Blyth, T., Mackinnon, I., Reid, M., Sarvana, O., Silver, D., Chen, A., Wang, L., Maggiore, L., Chang, O., Attaluri, N., Thornton, G., Chiu, C.-C., Bunyan, O., Levine, N., Chung, T., Eltyshev, E., Si, X., Lillicrap, T., Brady, D., Aggarwal, V., Wu, B., Xu, Y., McIlroy, R., Badola, K., Sandhu, P., Moreira, E., Stokowiec, W., Hemsley, R., Li, D., Tudor, A., Shyam, P., Rahimtoroghi, E., Haykal, S., Sprechmann, P., Zhou, X., Mincu, D., Li, Y., Addanki, R., Krishna, K., Wu, X., Frechette, A., Eyal, M., Dafoe, A., Lacey, D., Whang, J., Avrahami, T., Zhang, Y., Taropa,
  E., Lin, H., Toyama, D., Rutherford, E., Sano, M., Choe, H., Tomala, A., Safranek-Shrader, C., Kassner, N., Pajarskas, M., Harvey, M., Sechrist, S., Fortunato, M., Lyu, C., Elsayed, G., Kuang, C., Lottes, J., Chu, E., Jia, C., Chen, C.-W., Humphreys, P., Baumli, K., Tao, C., Samuel, R., dos Santos, C. N., Andreassen, A., Rakićević, N., Grewe, D., Kumar, A., Winkler, S., Caton, J., Brock, A., Dalmia, S., Sheahan, H., Barr, I., Miao, Y., Natsev, P., Devlin, J., Behbahani, F., Prost, F., Sun, Y., Myaskovsky, A., Pillai, T. S., Hurt, D., Lazaridou, A., Xiong, X., Zheng, C., Pardo, F., Li, X., Horgan, D., Stanton, J., Ambar, M., Xia, F., Lince, A., Wang, M., Mustafa, B., Webson, A., Lee, H., Anil, R., Wicke, M., Dozat, T., Sinha, A., Piqueras, E., Dabir, E., Upadhyay, S., Boral, A., Hendricks, L. A., Fry, C., Djolonga, J., Su, Y., Walker, J., Labanowski, J., Huang, R., Misra, V., Chen, J., Skerry-Ryan, R., Singh, A., Rijhwani, S., Yu, D., Castro-Ros, A., Changpinyo, B., Datta, R., Bagri, S., Hrafnkelsson,
  A. M., Maggioni, M., Zheng, D., Sulsky, Y., Hou, S., Paine, T. L., Yang, A., Riesa, J., Rogozinska, D., Marcus, D., Badawy, D. E., Zhang, Q., Wang, L., Miller, H., Greer, J., Sjos, L. L., Nova, A., Zen, H., Chaabouni, R., Rosca, M., Jiang, J., Chen, C., Liu, R., Sainath, T., Krikun, M., Polozov, A., Lespiau, J.-B., Newlan, J., Cankara, Z., Kwak, S., Xu, Y., Chen, P., Coenen, A., Meyer, C., Tsihlas, K., Ma, A., Gottweis, J., Xing, J., Gu, C., Miao, J., Frank, C., Cankara, Z., Ganapathy, S., Dasgupta, I., Hughes-Fitt, S., Chen, H., Reid, D., Rong, K., Fan, H., van Amersfoort, J., Zhuang, V., Cohen, A., Gu, S. S., Mohananey, A., Ilic, A., Tobin, T., Wieting, J., Bortsova, A., Thacker, P., Wang, E., Caveness, E., Chiu, J., Sezener, E., Kaskasoli, A., Baker, S., Millican, K., Elhawaty, M., Aisopos, K., Lebsack, C., Byrd, N., Dai, H., Jia, W., Wiethoff, M., Davoodi, E., Weston, A., Yagati, L., Ahuja, A., Gao, I., Pundak, G., Zhang, S., Azzam, M., Sim, K. C., Caelles, S., Keeling, J., Sharma, A., Swing, A., Li,
  Y., Liu, C., Bostock, C. G., Bansal, Y., Nado, Z., Anand, A., Lipschultz, J., Karmarkar, A., Proleev, L., Ittycheriah, A., Yeganeh, S. H., Polovets, G., Faust, A., Sun, J., Rrustemi, A., Li, P., Shivanna, R., Liu, J., Welty, C., Lebron, F., Baddepudi, A., Krause, S., Parisotto, E., Soricut, R., Xu, Z., Bloxwich, D., Johnson, M., Neyshabur, B., Mao-Jones, J., Wang, R., Ramasesh, V., Abbas, Z., Guez, A., Segal, C., Nguyen, D. D., Svensson, J., Hou, L., York, S., Milan, K., Bridgers, S., Gworek, W., Tagliasacchi, M., Lee-Thorp, J., Chang, M., Guseynov, A., Hartman, A. J., Kwong, M., Zhao, R., Kashem, S., Cole, E., Miech, A., Tanburn, R., Phuong, M., Pavetic, F., Cevey, S., Comanescu, R., Ives, R., Yang, S., Du, C., Li, B., Zhang, Z., Iinuma, M., Hu, C. H., Roy, A., Bijwadia, S., Zhu, Z., Martins, D., Saputro, R., Gergely, A., Zheng, S., Jia, D., Antonoglou, I., Sadovsky, A., Gu, S., Bi, Y., Andreev, A., Samangooei, S., Khan, M., Kocisky, T., Filos, A., Kumar, C., Bishop, C., Yu, A., Hodkinson, S., Mittal, S.,
  Shah, P., Moufarek, A., Cheng, Y., Bloniarz, A., Lee, J., Pejman, P., Michel, P., Spencer, S., Feinberg, V., Xiong, X., Savinov, N., Smith, C., Shakeri, S., Tran, D., Chesus, M., Bohnet, B., Tucker, G., von Glehn, T., Muir, C., Mao, Y., Kazawa, H., Slone, A., Soparkar, K., Shrivastava, D., Cobon-Kerr, J., Sharman, M., Pavagadhi, J., Araya, C., Misiunas, K., Ghelani, N., Laskin, M., Barker, D., Li, Q., Briukhov, A., Houlsby, N., Glaese, M., Lakshminarayanan, B., Schucher, N., Tang, Y., Collins, E., Lim, H., Feng, F., Recasens, A., Lai, G., Magni, A., Cao, N. D., Siddhant, A., Ashwood, Z., Orbay, J., Dehghani, M., Brennan, J., He, Y., Xu, K., Gao, Y., Saroufim, C., Molloy, J., Wu, X., Arnold, S., Chang, S., Schrittwieser, J., Buchatskaya, E., Radpour, S., Polacek, M., Giordano, S., Bapna, A., Tokumine, S., Hellendoorn, V., Sottiaux, T., Cogan, S., Severyn, A., Saleh, M., Thakoor, S., Shefey, L., Qiao, S., Gaba, M., yiin Chang, S., Swanson, C., Zhang, B., Lee, B., Rubenstein, P. K., Song, G., Kwiatkowski, T.,
  Koop, A., Kannan, A., Kao, D., Schuh, P., Stjerngren, A., Ghiasi, G., Gibson, G., Vilnis, L., Yuan, Y., Ferreira, F. T., Kamath, A., Klimenko, T., Franko, K., Xiao, K., Bhattacharya, I., Patel, M., Wang, R., Morris, A., Strudel, R., Sharma, V., Choy, P., Hashemi, S. H., Landon, J., Finkelstein, M., Jhakra, P., Frye, J., Barnes, M., Mauger, M., Daun, D., Baatarsukh, K., Tung, M., Farhan, W., Michalewski, H., Viola, F., de Chaumont Quitry, F., Lan, C. L., Hudson, T., Wang, Q., Fischer, F., Zheng, I., White, E., Dragan, A., baptiste Alayrac, J., Ni, E., Pritzel, A., Iwanicki, A., Isard, M., Bulanova, A., Zilka, L., Dyer, E., Sachan, D., Srinivasan, S., Muckenhirn, H., Cai, H., Mandhane, A., Tariq, M., Rae, J. W., Wang, G., Ayoub, K., FitzGerald, N., Zhao, Y., Han, W., Alberti, C., Garrette, D., Krishnakumar, K., Gimenez, M., Levskaya, A., Sohn, D., Matak, J., Iturrate, I., Chang, M. B., Xiang, J., Cao, Y., Ranka, N., Brown, G., Hutter, A., Mirrokni, V., Chen, N., Yao, K., Egyed, Z., Galilee, F., Liechty, T.,
  Kallakuri, P., Palmer, E., Ghemawat, S., Liu, J., Tao, D., Thornton, C., Green, T., Jasarevic, M., Lin, S., Cotruta, V., Tan, Y.-X., Fiedel, N., Yu, H., Chi, E., Neitz, A., Heitkaemper, J., Sinha, A., Zhou, D., Sun, Y., Kaed, C., Hulse, B., Mishra, S., Georgaki, M., Kudugunta, S., Farabet, C., Shafran, I., Vlasic, D., Tsitsulin, A., Ananthanarayanan, R., Carin, A., Su, G., Sun, P., V, S., Carvajal, G., Broder, J., Comsa, I., Repina, A., Wong, W., Chen, W. W., Hawkins, P., Filonov, E., Loher, L., Hirnschall, C., Wang, W., Ye, J., Burns, A., Cate, H., Wright, D. G., Piccinini, F., Zhang, L., Lin, C.-C., Gog, I., Kulizhskaya, Y., Sreevatsa, A., Song, S., Cobo, L. C., Iyer, A., Tekur, C., Garrido, G., Xiao, Z., Kemp, R., Zheng, H. S., Li, H., Agarwal, A., Ngani, C., Goshvadi, K., Santamaria-Fernandez, R., Fica, W., Chen, X., Gorgolewski, C., Sun, S., Garg, R., Ye, X., Eslami, S. M. A., Hua, N., Simon, J., Joshi, P., Kim, Y., Tenney, I., Potluri, S., Thiet, L. N., Yuan, Q., Luisier, F., Chronopoulou, A.,
  Scellato, S., Srinivasan, P., Chen, M., Koverkathu, V., Dalibard, V., Xu, Y., Saeta, B., Anderson, K., Sellam, T., Fernando, N., Huot, F., Jung, J., Varadarajan, M., Quinn, M., Raul, A., Le, M., Habalov, R., Clark, J., Jalan, K., Bullard, K., Singhal, A., Luong, T., Wang, B., Rajayogam, S., Eisenschlos, J., Jia, J., Finchelstein, D., Yakubovich, A., Balle, D., Fink, M., Agarwal, S., Li, J., Dvijotham, D., Pal, S., Kang, K., Konzelmann, J., Beattie, J., Dousse, O., Wu, D., Crocker, R., Elkind, C., Jonnalagadda, S. R., Lee, J., Holtmann-Rice, D., Kallarackal, K., Liu, R., Vnukov, D., Vats, N., Invernizzi, L., Jafari, M., Zhou, H., Taylor, L., Prendki, J., Wu, M., Eccles, T., Liu, T., Kopparapu, K., Beaufays, F., Angermueller, C., Marzoca, A., Sarcar, S., Dib, H., Stanway, J., Perbet, F., Trdin, N., Sterneck, R., Khorlin, A., Li, D., Wu, X., Goenka, S., Madras, D., Goldshtein, S., Gierke, W., Zhou, T., Liu, Y., Liang, Y., White, A., Li, Y., Singh, S., Bahargam, S., Epstein, M., Basu, S., Lao, L., Ozturel, A.,
  Crous, C., Zhai, A., Lu, H., Tung, Z., Gaur, N., Walton, A., Dixon, L., Zhang, M., Globerson, A., Uy, G., Bolt, A., Wiles, O., Nasr, M., Shumailov, I., Selvi, M., Piccinno, F., Aguilar, R., McCarthy, S., Khalman, M., Shukla, M., Galic, V., Carpenter, J., Villela, K., Zhang, H., Richardson, H., Martens, J., Bosnjak, M., Belle, S. R., Seibert, J., Alnahlawi, M., McWilliams, B., Singh, S., Louis, A., Ding, W., Popovici, D., Simicich, L., Knight, L., Mehta, P., Gupta, N., Shi, C., Fatehi, S., Mitrovic, J., Grills, A., Pagadora, J., Munkhdalai, T., Petrova, D., Eisenbud, D., Zhang, Z., Yates, D., Mittal, B., Tripuraneni, N., Assael, Y., Brovelli, T., Jain, P., Velimirovic, M., Akbulut, C., Mu, J., Macherey, W., Kumar, R., Xu, J., Qureshi, H., Comanici, G., Wiesner, J., Gong, Z., Ruddock, A., Bauer, M., Felt, N., GP, A., Arnab, A., Zelle, D., Rothfuss, J., Rosgen, B., Shenoy, A., Seybold, B., Li, X., Mudigonda, J., Erdogan, G., Xia, J., Simsa, J., Michi, A., Yao, Y., Yew, C., Kan, S., Caswell, I., Radebaugh, C.,
  Elisseeff, A., Valenzuela, P., McKinney, K., Paterson, K., Cui, A., Latorre-Chimoto, E., Kim, S., Zeng, W., Durden, K., Ponnapalli, P., Sosea, T., Choquette-Choo, C. A., Manyika, J., Robenek, B., Vashisht, H., Pereira, S., Lam, H., Velic, M., Owusu-Afriyie, D., Lee, K., Bolukbasi, T., Parrish, A., Lu, S., Park, J., Venkatraman, B., Talbert, A., Rosique, L., Cheng, Y., Sozanschi, A., Paszke, A., Kumar, P., Austin, J., Li, L., Salama, K., Perz, B., Kim, W., Dukkipati, N., Baryshnikov, A., Kaplanis, C., Sheng, X., Chervonyi, Y., Unlu, C., de Las Casas, D., Askham, H., Tunyasuvunakool, K., Gimeno, F., Poder, S., Kwak, C., Miecnikowski, M., Mirrokni, V., Dimitriev, A., Parisi, A., Liu, D., Tsai, T., Shevlane, T., Kouridi, C., Garmon, D., Goedeckemeyer, A., Brown, A. R., Vijayakumar, A., Elqursh, A., Jazayeri, S., Huang, J., Carthy, S. M., Hoover, J., Kim, L., Kumar, S., Chen, W., Biles, C., Bingham, G., Rosen, E., Wang, L., Tan, Q., Engel, D., Pongetti, F., de Cesare, D., Hwang, D., Yu, L., Pullman, J.,
  Narayanan, S., Levin, K., Gopal, S., Li, M., Aharoni, A., Trinh, T., Lo, J., Casagrande, N., Vij, R., Matthey, L., Ramadhana, B., Matthews, A., Carey, C., Johnson, M., Goranova, K., Shah, R., Ashraf, S., Dasgupta, K., Larsen, R., Wang, Y., Vuyyuru, M. R., Jiang, C., Ijazi, J., Osawa, K., Smith, C., Boppana, R. S., Bilal, T., Koizumi, Y., Xu, Y., Altun, Y., Shabat, N., Bariach, B., Korchemniy, A., Choo, K., Ronneberger, O., Iwuanyanwu, C., Zhao, S., Soergel, D., Hsieh, C.-J., Cai, I., Iqbal, S., Sundermeyer, M., Chen, Z., Bursztein, E., Malaviya, C., Biadsy, F., Shroff, P., Dhillon, I., Latkar, T., Dyer, C., Forbes, H., Nicosia, M., Nikolaev, V., Greene, S., Georgiev, M., Wang, P., Martin, N., Sedghi, H., Zhang, J., Banzal, P., Fritz, D., Rao, V., Wang, X., Zhang, J., Patraucean, V., Du, D., Mordatch, I., Jurin, I., Liu, L., Dubey, A., Mohan, A., Nowakowski, J., Ion, V.-D., Wei, N., Tojo, R., Raad, M. A., Hudson, D. A., Keshava, V., Agrawal, S., Ramirez, K., Wu, Z., Nguyen, H., Liu, J., Sewak, M., Petrini,
  B., Choi, D., Philips, I., Wang, Z., Bica, I., Garg, A., Wilkiewicz, J., Agrawal, P., Li, X., Guo, D., Xue, E., Shaik, N., Leach, A., Khan, S. M., Wiesinger, J., Jerome, S., Chakladar, A., Wang, A. W., Ornduff, T., Abu, F., Ghaffarkhah, A., Wainwright, M., Cortes, M., Liu, F., Maynez, J., Terzis, A., Samangouei, P., Mansour, R., Kepa, T., Aubet, F.-X., Algymr, A., Banica, D., Weisz, A., Orban, A., Senges, A., Andrejczuk, E., Geller, M., Santo, N. D., Anklin, V., Merey, M. A., Baeuml, M., Strohman, T., Bai, J., Petrov, S., Wu, Y., Hassabis, D., Kavukcuoglu, K., Dean, J., and Vinyals, O.
  Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context, 2024b.
  URL <https://arxiv.org/abs/2403.05530>.
- Wang et al. (2023)

  Wang, H., Fu, T., Du, Y., Gao, W., Huang, K., Liu, Z., Chandak, P., Liu, S., Van Katwyk, P., Deac, A., et al.
  Scientific discovery in the age of artificial intelligence.
  *Nature*, 620(7972):47–60, 2023.
- Wei et al. (2022a)

  Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., Yogatama, D., Bosma, M., Zhou, D., Metzler, D., Chi, E. H., Hashimoto, T., Vinyals, O., Liang, P., Dean, J., and Fedus, W.
  Emergent abilities of large language models, 2022a.
  URL <https://arxiv.org/abs/2206.07682>.
- Wei et al. (2022b)

  Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., Yogatama, D., Bosma, M., Zhou, D., Metzler, D., et al.
  Emergent abilities of large language models.
  *arXiv preprint arXiv:2206.07682*, 2022b.
- Wu & Lo (2024)

  Wu, T.-Y. and Lo, P.-Y.
  U-shaped and inverted-u scaling behind emergent abilities of large language models, 2024.
  URL <https://arxiv.org/abs/2410.01692>.
- Wu et al. (2024)

  Wu, Y., Sun, Z., Li, S., Welleck, S., and Yang, Y.
  Inference scaling laws: An empirical analysis of compute-optimal inference for problem-solving with language models, 2024.
  URL <https://arxiv.org/abs/2408.00724>.
- Xiong et al. (2023)

  Xiong, W., Liu, J., Molybog, I., Zhang, H., Bhargava, P., Hou, R., Martin, L., Rungta, R., Sankararaman, K. A., Oguz, B., Khabsa, M., Fang, H., Mehdad, Y., Narang, S., Malik, K., Fan, A., Bhosale, S., Edunov, S., Lewis, M., Wang, S., and Ma, H.
  Effective long-context scaling of foundation models, 2023.
  URL <https://arxiv.org/abs/2309.16039>.
- Zhai et al. (2022)

  Zhai, X., Kolesnikov, A., Houlsby, N., and Beyer, L.
  Scaling vision transformers.
  In *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, pp. 12104–12113, 2022.
- Zhang et al. (2024)

  Zhang, B., Liu, Z., Cherry, C., and Firat, O.
  When scaling meets llm finetuning: The effect of data, model and finetuning method, 2024.
  URL <https://arxiv.org/abs/2402.17193>.

## Appendix A Clarification of How Large Language Monkeys and Best-of-N Jailbreaking Sampled Data

In this manuscript, we used the phrasing of “independent attempts," which is not fully correct. In this appendix section, we clarify why we chose this terminology, what likely impacts we believe this inaccuracy may have had on our results, and how to correct the paper accordingly.

Large Language Monkeys ([Brown et al., 2024](#bib.bib21)) indeed drew 10,00010,000 independent attempts per problem, but Best-of-N Jailbreaking ([Hughes et al., 2024](#bib.bib54)) sampled data slightly different: for each problem, jailbreaking attempts were drawn until either a successful jailbreak was obtained or until a maximum limit of 10,00010,000 attempts was hit. Samples were also drawn in minibatches of size 60, making the (in)dependence of samples a bit tricky.

We omitted this nuance because it offers a second-order correction to our paper’s main story while offering little additional insight. Neither of our theorems and none of our main text figures change. We suspect that this slightly different sampling procedure explains why, in Fig. [6](#S4.F6 "Figure 6 ‣ 4 Lack of Distributional Structure Explains Deviations from Power Law Scaling"), the estimated power law exponents between the least squares power law estimator and the distributional power law estimator deviate more significantly from identity for Best-of-N Jailbreaking than for Large Language Monkeys. A natural way to correct for this is to use a [beta-negative binomial distribution](https://en.wikipedia.org/wiki/Beta_negative_binomial_distribution) rather than a [beta-binomial distribution](https://en.wikipedia.org/wiki/Beta-binomial_distribution), with an additional correction for the maximum number of attempts. For more information, please see Appendix [H](#A8 "Appendix H Maximum Likelihood Estimation of Scaled Beta-Negative Binomial Distribution").

## Appendix B Estimating Success Rates Using [Chen et al. (2021)](#bib.bib27)’s Estimator

In this manuscript, we defined passi​@​k\operatorname{pass_{i}@k} and ASRi​@​k\operatorname{ASR_{i}@k} as:

|  |  |  |  |
| --- | --- | --- | --- |
|  | passi​@​k\displaystyle\operatorname{pass_{i}@k} | =def𝔼k​ Attempts[𝕀[At least 1 attempt by the model solves the i-th problem]]\displaystyle\defeq\mathop{\mathbb{E}}_{k\text{ Attempts}}\big[\mathbb{I}[\text{At least 1 attempt by the model solves the $i$-th problem}]\big] |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  | ASRi​@​k\displaystyle\operatorname{ASR_{i}@k} | =def𝔼k​ Attempts[𝕀[At least 1 attempt jailbreaks the model on the i-th prompt]]\displaystyle\defeq\mathop{\mathbb{E}}_{k\text{ Attempts}}\big[\mathbb{I}[\text{At least 1 attempt jailbreaks the model on the $i$-th prompt}]\big] |  |

Throughout this manuscript, to estimate passi​@​k\operatorname{pass_{i}@k} and ASR​@​k\operatorname{ASR@k}, we used the unbiased and lower variance estimator introduced by [Chen et al. (2021)](#bib.bib27): for the ii-th problem, we sampled n≫kn\gg k attempts per problem, counted the number of successful attempts cc, and then swept kk to compute an estimate of passi​@​k\operatorname{pass_{i}@k} for different kk values:

|  |  |  |  |
| --- | --- | --- | --- |
|  | passi​@​k^=1−(n−ck)(nk)\widehat{\operatorname{pass_{i}@k}}=1-\frac{\binom{n-c}{k}}{\binom{n}{k}} |  | (12) |

Two comments: Firstly, nn as used here has no relationship with the number of problems in the benchmark (Sec. [1](#S1 "1 Introduction")), and secondly, our notation differs slightly from that of [Chen et al. (2021)](#bib.bib27), but the ideas are consistent. A numerically stable Python implementation of the estimator is provided in Fig. [8](#A2.F8 "Figure 8 ‣ Appendix B Estimating Success Rates Using ( ) ’s Estimator"):

[⬇](data:text/plain;base64,ICAgIGRlZiBlc3RpbWF0ZV9zdWNjZXNzX3JhdGVfYXRfa19wZXJfcHJvYmxlbShuOiBpbnQsIGM6IGludCwgazogaW50KSAtPiBmbG9hdDoKICAgICAgICAiIiIKICAgICAgICA6cGFyYW0gbjogbnVtYmVyIG9mIHRvdGFsIGF0dGVtcHRzIG9uIHRoaXMgcHJvYmxlbS4KICAgICAgICA6cGFyYW0gYzogbnVtYmVyIG9mIGNvcnJlY3QgYXR0ZW1wdHMgb24gdGhpcyBwcm9ibGVtLgogICAgICAgIDpwYXJhbSBrOiBrIGluIHBhc3NfaUAkayQuCiAgICAgICAgIiIiCiAgICAgICAgaWYgbiAtIGMgPCBrOiByZXR1cm4gMS4wCiAgICAgICAgcmV0dXJuIDEuMCAtIG5wLnByb2QoMS4wIC0gayAvIG5wLmFyYW5nZShuIC0gYyArIDEsIG4gKyAxKSkK)

def estimate_success_rate_at_k_per_problem(n: int, c: int, k: int) -> float:

"""

␣␣␣␣␣␣␣␣:param␣n:␣number␣of␣total␣attempts␣on␣this␣problem.

␣␣␣␣␣␣␣␣:param␣c:␣number␣of␣correct␣attempts␣on␣this␣problem.

␣␣␣␣␣␣␣␣:param␣k:␣k␣in␣pass_i@$k$.

␣␣␣␣␣␣␣␣"""

if n - c < k: return 1.0

return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

Figure 8: A numerically stable unbiased estimator of passi​@​k\operatorname{pass_{i}@k}, introduced by [Chen et al. (2021)](#bib.bib27).

To reiterate a point made by [Chen et al. (2021)](#bib.bib27), estimating passi​@​k\operatorname{pass_{i}@k} as 1−(1−passi​@​1^)k1-(1-\widehat{\operatorname{pass_{i}@1}})^{k} is biased (Fig. [9](#A2.F9 "Figure 9 ‣ Appendix B Estimating Success Rates Using ( ) ’s Estimator")).

Figure 9: Bias of Estimators of passi​@​k\operatorname{pass_{i}@k}. Numerical simulations show that estimating passi​@​k\operatorname{pass_{i}@k} as 1−(1−passi​@​1^)k1-(1-\widehat{\operatorname{pass_{i}@1}})^{k} is biased whereas the estimator of [Chen et al. (2021)](#bib.bib27) is not. For a mathematical proof of unbiasedness, see the original paper.

## Appendix C Fitting Power Laws to Large Language Monkeys and Best-of-N Jailbreaking

We fit power laws to a subset of data from Large Language Monkeys ([Brown et al., 2024](#bib.bib21)) and from Best-of-N Jailbreaking ([Hughes et al., 2024](#bib.bib54)), specifically Pythia language models ([Biderman et al., 2023](#bib.bib14)) on the MATH benchmark ([Hendrycks et al., 2021](#bib.bib46)) and frontier AI models – Claude, GPT4 ([OpenAI et al., 2024](#bib.bib78)), Gemini ([Team et al., 2024a](#bib.bib108); [Team et al., 2024b](#bib.bib109)) and Llama 3 ([Grattafiori et al., 2024](#bib.bib45)) – on the HarmBench jailbreaking benchmark ([Mazeika et al., 2024](#bib.bib69)). We show the functional forms and the fit parameters in Table [2](#A3.T2 "Table 2 ‣ Appendix C Fitting Power Laws to Large Language Monkeys and Best-of-N Jailbreaking") and Table [2](#A3.T2 "Table 2 ‣ Appendix C Fitting Power Laws to Large Language Monkeys and Best-of-N Jailbreaking") respectively. To fit the parameters, for Large Language Monkeys, we simply minimized the squared error between the actual and predicted −log⁡(pass𝒟​@​k)-\log(\operatorname{pass_{\mathcal{D}}@k}), and for Best-of-N Jailbreaking, we similarly minimized the squared error between the actual and predicted OPEN−log⁡(ASR𝒟​@​k))-\log(\operatorname{ASR_{\mathcal{D}}@k})).

Note: Llama 3 8B IT does not exhibit power law scaling under Best-of-N Jailbreaking (shown in Fig. [1](#S1.F1 "Figure 1 ‣ 1 Introduction"), bottom).

| Model | Benchmark | aa | bb |
| --- | --- | --- | --- |
| Pythia 70M | MATH | 8.026 | 0.194 |
| Pythia 160M | MATH | 6.591 | 0.280 |
| Pythia 410M | MATH | 5.524 | 0.286 |
| Pythia 1B | MATH | 5.452 | 0.315 |
| Pythia 2.8B | MATH | 4.104 | 0.336 |
| Pythia 6.9B | MATH | 4.255 | 0.348 |
| Pythia 12B | MATH | 4.113 | 0.370 |

Table 1: Large Language Monkeys ([Brown et al., 2024](#bib.bib21)) fitted power law parameters on 128 mathematical problems from MATH ([Hendrycks et al., 2021](#bib.bib46)).
  
Functional Form: −log⁡(pass𝒟​@​k)=a​k−b-\log(\operatorname{pass_{\mathcal{D}}@k})=a\,k^{-b}.

| Model | Modality | aa | bb |
| --- | --- | --- | --- |
| Claude 3.5 Opus | Text | 2.630 | 0.448 |
| Claude 3.5 Sonnet | Text | 3.436 | 0.312 |
| GPT4o | Text | 3.639 | 0.395 |
| GPT4o Mini | Text | 3.637 | 0.492 |
| Gemini 1.5 Flash | Text | 6.158 | 0.303 |
| Gemini 1.5 Pro | Text | 6.296 | 0.256 |
| Llama 3 8B IT | Text | – | – |

Table 2: Best-of-N Jailbreaking ([Hughes et al., 2024](#bib.bib54)) fitted power law parameters on text jailbreak prompts from HarmBench ([Mazeika et al., 2024](#bib.bib69)).
  
Functional Form: −log⁡(ASR𝒟​@​k)=a​k−b-\log(\operatorname{ASR_{\mathcal{D}}@k})=a\,k^{-b}.
  
Note: Llama 3 8B Instruction Tuned (IT) does not exhibit power law scaling.

## Appendix D Mathematical Equivalence Between Coverage and Average Success Rate

[Brown et al. (2024)](#bib.bib21) and [Hughes et al. (2024)](#bib.bib54) phrase their research in terms of “coverage", defined as the fraction of problems that can be solved or the fraction of prompts that can jailbreak a model, but as [Brown et al. (2024)](#bib.bib21) comment and we here derive, the coverage is mathematically equivalent to the average passi​@​k\operatorname{pass_{i}@k} (equivalently, ASR​@​k\operatorname{ASR@k}. due to two simple probabilistic primitives: (1) linearity of expectation, (2) the expectation of an indictor random variable of some event is the probability of said event and (3) the definition of passi​@​k\operatorname{pass_{i}@k}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼PromptsAttempts⁡[Coverage]\displaystyle\mathop{\raisebox{3.0pt}{$\mathbb{E}$}}_{\begin{subarray}{c}\text{Prompts}\\ \text{Attempts}\end{subarray}}\Big[\operatorname{Coverage}\Big] | =def𝔼ProblemsAttempts[Fraction of Problems Solved After k Attempts]\displaystyle\defeq\mathop{\raisebox{3.0pt}{$\mathbb{E}$}}_{\begin{subarray}{c}\text{Problems}\\ \text{Attempts}\end{subarray}}\Big[\text{Fraction of Problems Solved After $k$ Attempts}\Big] |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | =𝔼Problems⁡[𝔼Attempts|Problem⁡[𝕀⁡[Problem Solved After k Attempts]]]\displaystyle=\mathop{\raisebox{3.0pt}{$\mathbb{E}$}}_{\begin{subarray}{c}\text{Problems}\end{subarray}}\Bigg[\mathop{\raisebox{3.0pt}{$\mathbb{E}$}}_{\text{Attempts}|\text{Problem}}\Big[\mathbb{I}\big[\text{Problem Solved After $k$ Attempts}\big]\Big]\Bigg] |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | =𝔼Problems[passproblem​@​k]]\displaystyle=\mathop{\raisebox{3.0pt}{$\mathbb{E}$}}_{\begin{subarray}{c}\text{Problems}\end{subarray}}\Bigg[\operatorname{pass_{problem}@k}\Big]\Bigg] |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | =pass𝒟​@​k\displaystyle=\operatorname{pass_{\mathcal{D}}@k} |  |

In our work, we prefer phrasing along the lines of “success rate" over “coverage" because success rate avoids coverage’s binary implication that each problem/prompt is either “solved" or “not solved".

## Appendix E Aggregate Power Laws from a Probability Distribution over Exponential Functions

### E.1 Preliminaries: Power Laws from Weighted Exponential Functions

A known result is that power laws can emerge from appropriately weighted sums of exponential functions, e.g., ([Bochud & Challet, 2006](#bib.bib15); [Elkies, 2016](#bib.bib35); [Bousquet et al., 2020](#bib.bib19)). For a concrete example with a short proof:

|  |  |  |  |
| --- | --- | --- | --- |
|  | x−r=1Γ⁡(r)​∫0∞pr−1​e−p​x​𝑑p,x^{-r}=\frac{1}{\Gamma(r)}\int_{0}^{\infty}p^{r-1}\,e^{-px}\,dp, |  | (13) |

where Γ⁡(r)​=def​∫0∞sr−1​e−s​ds\Gamma(r)\defeq\int_{0}^{\infty}s^{r-1}\,e^{-s}\,ds is the [Gamma function](https://en.wikipedia.org/wiki/Gamma_function). The proof is via u-substitution u​=defp​xu\defeq p\,x:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 1Γ⁡(r)​∫0∞pr−1​e−p​x​𝑑p\displaystyle\frac{1}{\Gamma(r)}\int_{0}^{\infty}p^{r-1}\,e^{-px}\,dp | =1Γ⁡(r)​∫0∞(u/x)r−1​e−u​d​ux\displaystyle=\frac{1}{\Gamma(r)}\int_{0}^{\infty}(u/x)^{r-1}\,e^{-u}\,\frac{du}{x} |  | (14) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =1Γ⁡(r)​x−r​∫0∞ur−1​e−u​𝑑u\displaystyle=\frac{1}{\Gamma(r)}\,x^{-r}\,\int_{0}^{\infty}u^{r-1}\,e^{-u}\,du |  | (15) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =1Γ⁡(r)​x−r​Γ​(r)\displaystyle=\frac{1}{\Gamma(r)}\,x^{-r}\,\Gamma(r) |  | (16) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =x−r\displaystyle=x^{-r} |  | (17) |

In our particular context, we are interested in the scaling with kk of the expected success rate over problems sampled from the benchmark’s data distribution:

|  |  |  |  |
| --- | --- | --- | --- |
|  | pass𝒟​@​k⁡=def​𝔼passi​@​1∼𝒟⁡[passi​@​k]\operatorname{pass_{\mathcal{D}}@k}\defeq\mathop{\raisebox{3.0pt}{$\mathbb{E}$}}_{\operatorname{pass_{i}@1}\sim\mathcal{D}}\Big[\operatorname{pass_{i}@k}\Big] |  | (18) |

distribution (over problems in a benchmark) of passi​@​k\operatorname{pass_{i}@k} scores that yields power law scaling with respect to the number of attempts kk:

|  |  |  |  |
| --- | --- | --- | --- |
|  | −log⁡(1n​∑i=1npassi​@​k)≈a​k−b.-\log\Bigg(\frac{1}{n}\sum_{i=1}^{n}\operatorname{pass_{i}@k}\Bigg)\approx ak^{-b}. |  | (19) |

for constants a,b>0a,b>0.

### E.2 Delta Distribution: passi​@​1∼δ⁡(p),p∈(0,1)\operatorname{pass_{i}@1}\sim\delta(p),p\in(0,1)

To start with a negative result, we will show that not all distributions of the per-problem success probabilities passi​@​1\operatorname{pass_{i}@1} yield aggregate power law scaling.
Suppose that the model’s passi​@​1\operatorname{pass_{i}@1} probabilities across the benchmarks’ problems are all exactly p∈(0,1)p\in(0,1). For brevity, let pi​=defpassi​@​1p_{i}\defeq\operatorname{pass_{i}@1}. Then the aggregate success rate is:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝔼pi∼δ⁡(p)​[passi​@​k]\displaystyle\mathbb{E}_{p_{i}\sim\delta(p)}[\operatorname{pass_{i}@k}] | =1−𝔼pi​[(1−pi)k]\displaystyle=1-\mathbb{E}_{p_{i}}[(1-p_{i})^{k}] |  | (20) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =∫01δ⁡(p)​(1−pi)k​d​pi\displaystyle=\int_{0}^{1}\delta(p)\,(1-p_{i})^{k}\,dp_{i} |  | (21) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =(1−p)k.\displaystyle=(1-p)^{k}. |  | (22) |

Recalling that the expansion of log⁡(⋅)\log(\cdot) for small xx is −log⁡(1−x)=x+O⁡(x2)-\log(1-x)=x+O(x^{2}), in our case, we obtain:

|  |  |  |  |
| --- | --- | --- | --- |
|  | −log⁡(1−𝔼pi∼δ⁡(p)​[pass​@​k])=(1−p)k+O⁡((1−p)2​k)=(1−p)k+o⁡((1−p)k).-\log\Big(1-\mathbb{E}_{p_{i}\sim\delta(p)}[\operatorname{pass@k}]\Big)=(1-p)^{k}+O((1-p)^{2k})=(1-p)^{k}+o((1-p)^{k}). |  | (23) |

Thus, in the large kk regime, we find the negative log aggregate success rate exhibits exponential scaling with kk as we intuitively expect.

### E.3 Uniform Distribution: passi​@​1∼Uniform⁡(α,β)\operatorname{pass_{i}@1}\sim\mathrm{Uniform}(\alpha,\beta)

Suppose passi​@​1\operatorname{pass_{i}@1} probabilities follow a uniform distribution Uniform⁡(α,β)\mathrm{Uniform}(\alpha,\beta) where 0≤α<β≤10\leq\alpha<\beta\leq 1. The aggregate success rate after kk attempts is defined as:

|  |  |  |
| --- | --- | --- |
|  | passUniform⁡(α,β)⁡@​k​=def1−𝔼⁡[(1−p)k].\operatorname{pass_{\mathrm{Uniform}(\alpha,\beta)}}@k\defeq 1-\mathbb{E}\bigl[(1-p)^{k}\bigr]. |  |

If p∼Uniform⁡(α,β)p\sim\mathrm{Uniform}(\alpha,\beta), the expectation of (1−p)k(1-p)^{k} is:

|  |  |  |
| --- | --- | --- |
|  | 𝔼⁡[(1−p)k]=1β−α​∫αβ(1−p)k​𝑑p.\mathbb{E}\bigl[(1-p)^{k}\bigr]\;=\;\frac{1}{\beta-\alpha}\int_{\alpha}^{\beta}(1-p)^{k}\,\mathrm{d}p. |  |

Evaluating the integral gives:

|  |  |  |
| --- | --- | --- |
|  | 𝔼⁡[(1−p)k]=(1−α)k+1−(1−β)k+1(β−α)⋅(k+1).\mathbb{E}\bigl[(1-p)^{k}\bigr]\;=\;\frac{(1-\alpha)^{k+1}-(1-\beta)^{k+1}}{(\beta-\alpha)\cdot(k+1)}. |  |

Thus, the aggregate success rate becomes:

|  |  |  |
| --- | --- | --- |
|  | passUniform⁡(α,β)⁡@​k= 1−(1−α)k+1−(1−β)k+1(β−α)⋅(k+1).\operatorname{pass_{\mathrm{Uniform}(\alpha,\beta)}}@k\;=\;1\;-\;\frac{(1-\alpha)^{k+1}-(1-\beta)^{k+1}}{(\beta-\alpha)\cdot(k+1)}. |  |

#### Case A: α>0\alpha>0

If α>0\alpha>0, then both (1−α)(1-\alpha) and (1−β)(1-\beta) are strictly less than 11. As k→∞k\to\infty, (1−α)k+1(1-\alpha)^{k+1} and (1−β)k+1(1-\beta)^{k+1} decay exponentially. Hence:

|  |  |  |
| --- | --- | --- |
|  | 𝔼⁡[(1−p)k]∼(1−α)k+1(β−α)⋅(k+1),\mathbb{E}\bigl[(1-p)^{k}\bigr]\sim\frac{(1-\alpha)^{k+1}}{(\beta-\alpha)\cdot(k+1)}, |  |

and passUniform⁡(α,β)⁡@​k\operatorname{pass_{\mathrm{Uniform}(\alpha,\beta)}}@k approaches 11 exponentially fast:

|  |  |  |
| --- | --- | --- |
|  | passUniform⁡(α,β)⁡@​k∼1−(1−α)k+1(β−α)⋅(k+1).\operatorname{pass_{\mathrm{Uniform}(\alpha,\beta)}}@k\sim 1-\frac{(1-\alpha)^{k+1}}{(\beta-\alpha)\cdot(k+1)}. |  |

Thus, the negative log of the aggregate success rate decays exponentially:

|  |  |  |
| --- | --- | --- |
|  | −log⁡(passUniform⁡(α,β)⁡@​k)∼e−Ω⁡(k).-\log\bigl(\operatorname{pass_{\mathrm{Uniform}(\alpha,\beta)}}@k\bigr)\sim e^{-\Omega(k)}. |  |

#### Case B: α=0\alpha=0

When α=0\alpha=0, the uniform distribution is over [0,β][0,\beta]. In this case:

|  |  |  |
| --- | --- | --- |
|  | 𝔼⁡[(1−p)k]=1β⋅1−(1−β)k+1k+1.\mathbb{E}\bigl[(1-p)^{k}\bigr]\;=\;\frac{1}{\beta}\cdot\frac{1-(1-\beta)^{k+1}}{k+1}. |  |

For large kk, (1−β)k+1(1-\beta)^{k+1} becomes exponentially small, and:

|  |  |  |
| --- | --- | --- |
|  | 𝔼⁡[(1−p)k]∼1β⋅1k+1.\mathbb{E}\bigl[(1-p)^{k}\bigr]\sim\frac{1}{\beta}\cdot\frac{1}{k+1}. |  |

The aggregate success rate is then:

|  |  |  |
| --- | --- | --- |
|  | passUniform⁡(0,β)⁡@​k∼1−1β⋅k.\operatorname{pass_{\mathrm{Uniform}(0,\beta)}}@k\sim 1-\frac{1}{\beta\cdot k}. |  |

The negative log exhibits power-law scaling:

|  |  |  |
| --- | --- | --- |
|  | −log⁡(passUniform⁡(0,β)⁡@​k)∼1β⋅1k.-\log\bigl(\operatorname{pass_{\mathrm{Uniform}(0,\beta)}}@k\bigr)\sim\frac{1}{\beta}\cdot\frac{1}{k}. |  |

#### Special Case: Uniform⁡(0,1)\mathrm{Uniform}(0,1)

If β=1\beta=1, the distribution is uniform on [0,1][0,1]. In this case:

|  |  |  |
| --- | --- | --- |
|  | 𝔼⁡[(1−p)k]=1k+1,\mathbb{E}\bigl[(1-p)^{k}\bigr]\;=\;\frac{1}{k+1}, |  |

and the success rate becomes:

|  |  |  |
| --- | --- | --- |
|  | passUniform⁡(0,1)⁡@​k= 1−1k+1.\operatorname{pass_{\mathrm{Uniform}(0,1)}}@k\;=\;1-\frac{1}{k+1}. |  |

For large kk:

|  |  |  |
| --- | --- | --- |
|  | −log⁡(passUniform⁡(0,1)⁡@​k)∼1k.-\log\bigl(\operatorname{pass_{\mathrm{Uniform}(0,1)}}@k\bigr)\sim\frac{1}{k}. |  |

### E.4 2-Parameter Beta Distribution: passi​@​1∼Beta⁡(α,β)\operatorname{pass_{i}@1}\sim\operatorname{Beta}(\alpha,\beta)

Suppose that the model’s passi​@​1\operatorname{pass_{i}@1} probabilities across the benchmark problems follow a Beta distribution:

|  |  |  |
| --- | --- | --- |
|  | passi​@​1∼Beta⁡(α,β)\operatorname{pass_{i}@1}\sim\operatorname{Beta}(\alpha,\beta) |  |

The probability density function of this distribution over the support x∈(0,1)x\in(0,1) is:

|  |  |  |  |
| --- | --- | --- | --- |
|  | f⁡(x,α,β)​=def1B⁡(α,β)​xα−1​(1−x)β−1,f(x;\alpha,\beta)\defeq\frac{1}{B(\alpha,\beta)}\,x^{\alpha-1}\,(1-x)^{\beta-1}, |  | (24) |

where α>0,β>0\alpha>0,\beta>0 and B⁡(⋅,⋅)B(\cdot,\cdot) is the [Beta function](https://en.wikipedia.org/wiki/Beta_function). For brevity, let pi​=defpassi​@​1p_{i}\defeq\operatorname{pass_{i}@1}. Under our assumed Beta distribution:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | passBeta⁡(α,β)​@​k\displaystyle\operatorname{pass_{\operatorname{Beta(\alpha,\beta)}}@k} | =def1−𝔼pi∼Beta⁡(α,β)​[(1−pi)k]\displaystyle\defeq 1-\mathbb{E}_{p_{i}\sim\operatorname{Beta(\alpha,\beta)}}[(1-p_{i})^{k}] |  | (25) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =1−∫01piα−1​(1−pi)β−1B⁡(α,β)​(1−pi)k​d​pi\displaystyle=1-\int_{0}^{1}\frac{p_{i}^{\alpha-1}(1-p_{i})^{\beta-1}}{B(\alpha,\beta)}\;(1-p_{i})^{k}\;dp_{i} |  | (26) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =1−Γ⁡(α+β)Γ⁡(α)​Γ​(β)​Γ⁡(α)​Γ​(β+k)Γ⁡(α+β+k)\displaystyle=1-\frac{\Gamma(\alpha+\beta)}{\Gamma(\alpha)\Gamma(\beta)}\frac{\Gamma(\alpha)\Gamma(\beta+k)}{\Gamma(\alpha+\beta+k)} |  | (27) |

where Γ⁡(⋅)\Gamma(\cdot) is again the Gamma function. The Γ⁡(α)\Gamma(\alpha) terms cancel, and a standard asymptotic result of the gamma function for large kk tells us that:

|  |  |  |  |
| --- | --- | --- | --- |
|  | Γ⁡(β+k)Γ⁡(α+β+k)∼k−α,\frac{\Gamma(\beta+k)}{\Gamma(\alpha+\beta+k)}\sim k^{-\alpha}, |  | (28) |

and thus:

|  |  |  |  |
| --- | --- | --- | --- |
|  | Γ⁡(α+β)Γ⁡(β)​Γ⁡(β+k)Γ⁡(α+β+k)∼Γ⁡(α+β)Γ⁡(β)​k−α.\frac{\Gamma(\alpha+\beta)}{\Gamma(\beta)}\frac{\Gamma(\beta+k)}{\Gamma(\alpha+\beta+k)}\sim\frac{\Gamma(\alpha+\beta)}{\Gamma(\beta)}k^{-\alpha}. |  | (29) |

Recalling again that the expansion of log⁡(⋅)\log(\cdot) for small xx is −log⁡(1−x)=x+O⁡(x2)-\log(1-x)=x+O(x^{2}), in our case, we obtain:

|  |  |  |  |
| --- | --- | --- | --- |
|  | −log⁡(pass𝒟​@​k)=Γ⁡(α+β)Γ⁡(β)​k−α+O⁡(k−2​α)=Γ⁡(α+β)Γ⁡(β)​k−α+o⁡(k−α).-\log\Big(\operatorname{pass_{\mathcal{D}}@k}\Big)=\frac{\Gamma(\alpha+\beta)}{\Gamma(\beta)}k^{-\alpha}+O(k^{-2\alpha})=\frac{\Gamma(\alpha+\beta)}{\Gamma(\beta)}k^{-\alpha}+o(k^{-\alpha}). |  | (30) |

From this final result, we see that under a Beta distribution and in the large kk regime, the negative log aggregate success rate exhibits polynomial (power-law) scaling with kk for exponent α\alpha

### E.5 Kumaraswamy Distribution: passi​@​1∼Kumaraswamy⁡(α,β)\operatorname{pass_{i}@1}\sim\operatorname{Kumaraswamy}(\alpha,\beta)

Next, suppose the model’s passi​@​1\operatorname{pass_{i}@1} probabilities follow a Kumaraswamy distribution. The probability density function of this distribution over the support x∈(0,1)x\in(0,1) is:

|  |  |  |  |
| --- | --- | --- | --- |
|  | f⁡(x,α,β)​=defα​β​xα−1​(1−xα)β−1f(x;\alpha,\beta)\defeq\alpha\,\beta\,x^{\alpha-1}\,(1-x^{\alpha})^{\beta-1} |  | (31) |

Again for brevity, let pi​=defpassi​@​1p_{i}\defeq\operatorname{pass_{i}@1}. Under our assumed Kumaraswamy distribution:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | passKumaraswamy⁡(α,β)​@​k\displaystyle\operatorname{pass_{\operatorname{Kumaraswamy(\alpha,\beta)}}@k} | =def1−𝔼pi∼Kumaraswamy⁡(α,β)​[(1−pi)k]\displaystyle\defeq 1-\mathbb{E}_{p_{i}\sim\operatorname{Kumaraswamy}(\alpha,\beta)}[(1-p_{i})^{k}] |  | (32) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =1−∫01(1−p)k⋅α​β​pα−1​(1−pα)β−1​𝑑p.\displaystyle=1-\int_{0}^{1}(1-p)^{k}\cdot\alpha\,\beta\,p^{\alpha-1}\,(1-p^{\alpha})^{\beta-1}dp. |  | (33) |

Define the integral

|  |  |  |  |
| --- | --- | --- | --- |
|  | Ik​=def𝔼⁡((1−p)k)=∫01(1−x)k​α​β​xα−1​(1−xα)β−1​dx.I_{k}\defeq\mathbb{E}\bigl((1-p)^{k}\bigr)=\int_{0}^{1}(1-x)^{k}\,\alpha\,\beta\;x^{\alpha-1}\;\bigl(1-x^{\alpha}\bigr)^{\beta-1}\;\mathrm{d}x. |  | (34) |

We aim to analyze IkI_{k} for large kk. Notice that (1−x)k(1-x)^{k} is exponentially small in kk unless xx is very close to 0. Thus, intuitively, most of the contribution to IkI_{k} arises from x∈[0,O⁡(1/k)]x\in[0,\,O(1/k)].

#### Step 1: Split the integral into two parts.

Fix a constant c>0c>0. Write

|  |  |  |
| --- | --- | --- |
|  | Ik=∫0c/k[⋯]​𝑑x+∫c/k1[⋯]​𝑑x​=defIk,left+Ik,right,I_{k}\;=\;\int_{0}^{c/k}[\cdots]\,\mathrm{d}x\;+\;\int_{c/k}^{1}[\cdots]\,\mathrm{d}x\;\;\defeq\;\;I_{k,\mathrm{left}}\;+\;I_{k,\mathrm{right}}, |  |

where [⋯][\cdots] indicates the same integrand.
In the region x∈[c/k,1]x\in[c/k,1], we have (1−x)k≤e−k​x≤e−c(1-x)^{k}\leq e^{-k\,x}\leq e^{-c}. Hence Ik,right=O⁡(e−c)I_{k,\mathrm{right}}=O\bigl(e^{-c}\bigr). Since cc can be made arbitrarily large, Ik,rightI_{k,\mathrm{right}} becomes negligible compared to any polynomial in 1/k1/k.

#### Step 2: Approximate the integrand in the small-xx region.

On [0,c/k][0,c/k], we use the approximation log⁡(1−x)=−x+O⁡(x2)\log(1-x)=-x+O(x^{2}). Thus

|  |  |  |
| --- | --- | --- |
|  | (1−x)k=exp⁡(k​log⁡(1−x))=exp⁡(−k​x+O⁡(k​x2)).(1-x)^{k}=\exp\big(k\log(1-x)\big)=\exp\big(-k\,x+O(k\,x^{2})\big). |  |

Since x≤c/kx\leq c/k implies k​x2≤c2/k=O⁡(1/k)k\,x^{2}\leq c^{2}/k=O(1/k), and exp⁡(ϵ)=1+O⁡(ϵ)\exp(\epsilon)=1+O(\epsilon), we get

|  |  |  |
| --- | --- | --- |
|  | (1−x)k=exp⁡(−k​x)​exp⁡(O⁡(1/k))=exp⁡(−k​x)​(1+O⁡(1k)).(1-x)^{k}=\exp(-k\,x)\exp(O(1/k))=\exp(-k\,x)\,\big(1+O\bigl(\tfrac{1}{k}\bigr)\big). |  |

Furthermore, since (1−y)m=1−m​y+O⁡(y2)(1-y)^{m}=1-my+O(y^{2}), for small xx

|  |  |  |
| --- | --- | --- |
|  | (1−xα)β−1=1−(β−1)​xα+O⁡(x2​α)=1+O⁡(xα).\,(1-x^{\alpha})^{\beta-1}=1-(\beta-1)x^{\alpha}+O(x^{2\alpha})=1+O\bigl(x^{\alpha}\bigr). |  |

In the region x≤c/kx\leq c/k, that error is O⁡(k−α)O\bigl(k^{-\alpha}\bigr).
Hence, within the small-xx region, the integrand

|  |  |  |
| --- | --- | --- |
|  | (1−x)k​α​β​xα−1​(1−xα)β−1(1-x)^{k}\;\alpha\,\beta\;x^{\alpha-1}\;\bigl(1-x^{\alpha}\bigr)^{\beta-1} |  |

can be approximated by

|  |  |  |
| --- | --- | --- |
|  | α​β​xα−1​e−k​x+O⁡(k−α​xα−1​e−k​x).\alpha\,\beta\;x^{\alpha-1}\;e^{-k\,x}\;+\;O\Bigl(k^{-\alpha}\,x^{\alpha-1}\,e^{-k\,x}\Bigr). |  |

Thus

|  |  |  |
| --- | --- | --- |
|  | Ik,left=∫0c/kα​β​xα−1​e−k​x​𝑑x+O⁡(k−α​∫0c/kxα−1​e−k​x​𝑑x)+O⁡(e−c).\displaystyle I_{k,\mathrm{left}}\;=\;\int_{0}^{c/k}\alpha\,\beta\;x^{\alpha-1}\,e^{-k\,x}\;\mathrm{d}x\;+\;O\Bigl(k^{-\alpha}\int_{0}^{c/k}x^{\alpha-1}\,e^{-k\,x}\,\mathrm{d}x\Bigr)\;+\;O\bigl(e^{-c}\bigr). |  |

#### Step 3: Substitution u​=defk​x\,u\defeq k\,x.

To handle
∫0c/kxα−1​e−k​x​𝑑x\int_{0}^{c/k}x^{\alpha-1}e^{-k\,x}\,\mathrm{d}x,
we substitute u=k​xu=k\,x. Then x=u/kx=u/k, d​x=d​u/k\mathrm{d}x=\mathrm{d}u/k, and the upper limit x=c/kx=c/k becomes u=cu=c. Hence,

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∫0c/kxα−1​e−k​x​𝑑x\displaystyle\int_{0}^{c/k}x^{\alpha-1}\,e^{-k\,x}\,\mathrm{d}x | =∫0c(uk)α−1​e−u​d​uk\displaystyle=\;\int_{0}^{c}\Bigl(\tfrac{u}{k}\Bigr)^{\alpha-1}\,e^{-\,u}\;\frac{\mathrm{d}u}{k} |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | =k−α​∫0cuα−1​e−u​𝑑u.\displaystyle=\;k^{-\alpha}\int_{0}^{c}u^{\alpha-1}\,e^{-\,u}\;\mathrm{d}u. |  |

As c→∞c\to\infty, ∫0cuα−1​e−u​𝑑u→Γ⁡(α)\int_{0}^{c}u^{\alpha-1}e^{-\,u}\,\mathrm{d}u\to\Gamma(\alpha), and for finite cc the remainder is O⁡(e−c)O\bigl(e^{-\,c}\bigr). Therefore,

|  |  |  |
| --- | --- | --- |
|  | ∫01xα−1​e−k​x​𝑑x=k−α​Γ​(α)+O⁡(k−α​e−c),\int_{0}^{1}x^{\alpha-1}\,e^{-k\,x}\,\mathrm{d}x=k^{-\alpha}\,\Gamma(\alpha)\;+\;O\bigl(k^{-\alpha}\,e^{-\,c}\bigr), |  |

and absorbing the constant cc into big-OO notation gives

|  |  |  |
| --- | --- | --- |
|  | ∫01xα−1​e−k​x​𝑑x=k−α​Γ​(α)+O⁡(k−α−ϵ)for some ​ϵ>0.\int_{0}^{1}x^{\alpha-1}\,e^{-k\,x}\,\mathrm{d}x=k^{-\alpha}\,\Gamma(\alpha)\;+\;O\bigl(k^{-\alpha-\epsilon}\bigr)\quad\text{for some }\epsilon>0. |  |

Multiplying by the factor α​β\alpha\,\beta, we deduce that

|  |  |  |
| --- | --- | --- |
|  | Ik=α​β​Γ​(α)​k−α+O⁡(k−α−ϵ).I_{k}\;=\;\alpha\,\beta\,\Gamma(\alpha)\,k^{-\alpha}\;+\;O\bigl(k^{-\alpha-\epsilon}\bigr). |  |

#### Step 4: Final conclusion for the success rate.

Recall
passKumaraswamy⁡(α,β)​@​k=1−Ik\operatorname{pass_{\mathrm{Kumaraswamy}(\alpha,\beta)}@k}=1-I_{k}. Hence

|  |  |  |
| --- | --- | --- |
|  | passKumaraswamy⁡(α,β)​@​k= 1−α​β​Γ​(α)​k−α+O⁡(k−α−ϵ).\operatorname{pass_{\mathrm{Kumaraswamy}(\alpha,\beta)}@k}\;=\;1\;-\;\alpha\,\beta\,\Gamma(\alpha)\,k^{-\alpha}\;+\;O\bigl(k^{-\alpha-\epsilon}\bigr). |  |

Since this tends to 1, its negative log is governed by the magnitude of
α​β​Γ​(α)​k−α\,\alpha\,\beta\,\Gamma(\alpha)\,k^{-\alpha}. Using the expansion
−log⁡(1−y)=y+O⁡(y2)-\log(1-y)=y+O(y^{2}) as y→0y\to 0, we get

|  |  |  |
| --- | --- | --- |
|  | −log⁡(passKumaraswamy⁡(α,β)​@​k)=α​β​Γ​(α)​k−α+o⁡(k−α).-\log\Big(\operatorname{pass_{\mathrm{Kumaraswamy}(\alpha,\beta)}@k}\Big)\;=\;\alpha\,\beta\,\Gamma(\alpha)\;k^{-\alpha}\;+\;o\bigl(k^{-\alpha}\bigr). |  |

That is precisely polynomial (power-law) decay in the negative log success rate with exponent α\alpha.

### E.6 Continuous Bernoulli Distribution: passi​@​1∼ContinousBernoulli⁡(λ)\operatorname{pass_{i}@1}\sim\operatorname{ContinousBernoulli}(\lambda)

Next, suppose the model’s passi​@​1\operatorname{pass_{i}@1} probabilities follow a Continuous Bernoulli distribution. The probability density function of this distribution over the support x∈[0,1]x\in[0,1] is:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | f⁡(x,λ)\displaystyle f(x;\lambda) | =defC⁡(λ)​λx​(1−λ)1−x\displaystyle\defeq C(\lambda)\lambda^{x}(1-\lambda)^{1-x} |  | (35) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | C⁡(λ)\displaystyle C(\lambda) | =def{2 if ​λ=1/22​tanh−1⁡(1−2​λ)1−2​λotherwise.\displaystyle\defeq\begin{cases}2&\text{ if }\lambda=1/2\\ \frac{2\tanh^{-1}{(1-2\lambda)}}{1-2\lambda}&\text{otherwise}\end{cases}. |  | (36) |

The density can equivalently be rewritten in a more convenient form for our purposes:

|  |  |  |  |
| --- | --- | --- | --- |
|  | f⁡(x,λ)=C⁡(λ)​λx​(1−λ)​(1−λ)−x=C⁡(λ)​(1−λ)​(λ1−λ)xf(x;\lambda)=C(\lambda)\lambda^{x}(1-\lambda)(1-\lambda)^{-x}=C(\lambda)(1-\lambda)\Big(\frac{\lambda}{1-\lambda}\Big)^{x} |  | (37) |

Because the individual success probability is low in our data, we shall consider the small λ<1/2\lambda<1/2 regime. We follow the same approach as with the Kumaraswamy distribution.

#### Step 1: Write the aggregate pass rate.

The aggregate pass rate is defined as:

|  |  |  |
| --- | --- | --- |
|  | passContinuousBernoulli⁡(λ)​@​k=1−Ik,whereIk​=def​∫01(1−p)k​f​(p,λ)​dp.\operatorname{pass_{ContinuousBernoulli(\lambda)}@k}=1-I_{k},\quad\text{where}\quad I_{k}\defeq\int_{0}^{1}(1-p)^{k}\,f(p;\lambda)\,dp. |  |

Substituting the density f⁡(p,λ)f(p;\lambda), we get:

|  |  |  |
| --- | --- | --- |
|  | Ik=∫01(1−p)k​C​(λ)​λp​(1−λ)1−p​𝑑p.I_{k}=\int_{0}^{1}(1-p)^{k}\,C(\lambda)\,\lambda^{p}\,(1-\lambda)^{1-p}\,dp. |  |

#### Step 2: Simplify using an exponential form.

Using the exponential rewriting:

|  |  |  |
| --- | --- | --- |
|  | λp​(1−λ)1−p=(1−λ)​exp⁡(p​log⁡(λ1−λ)),\lambda^{p}\,(1-\lambda)^{1-p}=(1-\lambda)\exp\Bigl(p\log\bigl(\tfrac{\lambda}{1-\lambda}\bigr)\Bigr), |  |

the integral becomes:

|  |  |  |
| --- | --- | --- |
|  | Ik=C⁡(λ)​(1−λ)​∫01(1−p)k​exp⁡(p​log⁡(λ1−λ))​𝑑p.I_{k}=C(\lambda)\,(1-\lambda)\int_{0}^{1}(1-p)^{k}\exp\Bigl(p\log\bigl(\tfrac{\lambda}{1-\lambda}\bigr)\Bigr)\,dp. |  |

#### Step 3: Dominance of the small-pp region.

For large kk, (1−p)k(1-p)^{k} decays exponentially unless pp is close to 0. Thus, the main contribution to the integral arises from the region p∈[0,c/k]p\in[0,c/k], where c>0c>0 is a constant. Decompose the integral:

|  |  |  |
| --- | --- | --- |
|  | Ik=∫0c/k[⋯]​𝑑p+∫c/k1[⋯]​𝑑p​=defIk,left+Ik,right.I_{k}=\int_{0}^{c/k}[\cdots]\,dp+\int_{c/k}^{1}[\cdots]\,dp\defeq I_{k,\mathrm{left}}+I_{k,\mathrm{right}}. |  |

In the region p∈[c/k,1]p\in[c/k,1], we have (1−p)k≤e−k​p≤e−c(1-p)^{k}\leq e^{-kp}\leq e^{-c}, making Ik,right=O⁡(e−c)I_{k,\mathrm{right}}=O(e^{-c}), which is negligible compared to 1/k1/k. Thus, we focus on Ik,leftI_{k,\mathrm{left}}:

|  |  |  |
| --- | --- | --- |
|  | Ik,left=C⁡(λ)​(1−λ)​∫0c/k(1−p)k​exp⁡(p​log⁡(λ1−λ))​𝑑p.I_{k,\mathrm{left}}=C(\lambda)\,(1-\lambda)\int_{0}^{c/k}(1-p)^{k}\exp\Bigl(p\log\bigl(\tfrac{\lambda}{1-\lambda}\bigr)\Bigr)\,dp. |  |

#### Step 4: Approximate the integrand.

For p∈[0,c/k]p\in[0,c/k], use the same approximations from the Kumaraswamy derivation:

|  |  |  |
| --- | --- | --- |
|  | (1−p)k=e−k​p​(1+O⁡(p)),exp⁡(p​log⁡(λ1−λ))=1+O⁡(p).(1-p)^{k}=e^{-kp}\,\bigl(1+O(p)\bigr),\quad\exp\Bigl(p\log\bigl(\tfrac{\lambda}{1-\lambda}\bigr)\Bigr)=1+O(p). |  |

Thus, the integrand becomes:

|  |  |  |
| --- | --- | --- |
|  | (1−p)k​exp⁡(p​log⁡(λ1−λ))=e−k​p​(1+O⁡(p)).(1-p)^{k}\exp\Bigl(p\log\bigl(\tfrac{\lambda}{1-\lambda}\bigr)\Bigr)=e^{-kp}\,\bigl(1+O(p)\bigr). |  |

#### Step 5: Change of variables.

Let u​=defkpu\defeq kp, so p=u/kp=u/k and d​p=d​u/kdp=du/k. The integral becomes:

|  |  |  |
| --- | --- | --- |
|  | Ik,left=C⁡(λ)​(1−λ)​∫0ce−u​(1+O⁡(u/k))​d​uk.I_{k,\mathrm{left}}=C(\lambda)\,(1-\lambda)\int_{0}^{c}e^{-u}\,\bigl(1+O(u/k)\bigr)\,\frac{du}{k}. |  |

Split the integral:

|  |  |  |
| --- | --- | --- |
|  | Ik,left=C​(λ)​(1−λ)k​∫0ce−u​𝑑u+O⁡(1k2).I_{k,\mathrm{left}}=\frac{C(\lambda)\,(1-\lambda)}{k}\int_{0}^{c}e^{-u}\,du+O\Bigl(\frac{1}{k^{2}}\Bigr). |  |

As c→∞c\to\infty, ∫0ce−u​𝑑u→1\int_{0}^{c}e^{-u}\,du\to 1. Thus:

|  |  |  |
| --- | --- | --- |
|  | Ik,left=C​(λ)​(1−λ)k+O⁡(1k2).I_{k,\mathrm{left}}=\frac{C(\lambda)\,(1-\lambda)}{k}+O\Bigl(\frac{1}{k^{2}}\Bigr). |  |

Since Ik,right=O⁡(e−c)I_{k,\mathrm{right}}=O(e^{-c}) is negligible, we have:

|  |  |  |
| --- | --- | --- |
|  | Ik=C​(λ)​(1−λ)k+O⁡(1k2).I_{k}=\frac{C(\lambda)\,(1-\lambda)}{k}+O\Bigl(\frac{1}{k^{2}}\Bigr). |  |

#### Step 7: Final conclusion for the success rate.

Recall:

|  |  |  |
| --- | --- | --- |
|  | passContinuousBernoulli⁡(λ)​@​k=1−Ik.\operatorname{pass_{ContinuousBernoulli(\lambda)}@k}=1-I_{k}. |  |

For large kk, this implies:

|  |  |  |
| --- | --- | --- |
|  | passContinuousBernoulli⁡(λ)​@​k=1−C​(λ)​(1−λ)k+O⁡(1k2).\operatorname{pass_{ContinuousBernoulli(\lambda)}@k}=1-\frac{C(\lambda)\,(1-\lambda)}{k}+O\Bigl(\frac{1}{k^{2}}\Bigr). |  |

Using the expansion −log⁡(1−y)=y+O⁡(y2)-\log(1-y)=y+O(y^{2}) for small yy, we find:

|  |  |  |
| --- | --- | --- |
|  | −log⁡(passContinuousBernoulli⁡(λ)​@​k)=C⁡(λ)​(1−λ)​k−1+o⁡(k−1).-\log\bigl(\operatorname{pass_{ContinuousBernoulli(\lambda)}@k}\bigr)=C(\lambda)\,(1-\lambda)k^{-1}+o(k^{-1}). |  |

That is precisely polynomial (power-law) decay in the negative log success rate with exponent −1-1.

As a side comment, recall that tanh−1⁡(x)=12​log⁡(1+x1−x)\tanh^{-1}(x)=\frac{1}{2}\log\big(\frac{1+x}{1-x}\big), the normalizing constant C⁡(λ)C(\lambda) can be rewritten as:

|  |  |  |  |
| --- | --- | --- | --- |
|  | C⁡(λ)=21−2​λ​12​log⁡(1+(1−2​λ)1−(1−2​λ))=11−2​λ​log⁡(1−λλ).C(\lambda)=\frac{2}{1-2\lambda}\frac{1}{2}\log\Bigg(\frac{1+(1-2\lambda)}{1-(1-2\lambda)}\Bigg)=\frac{1}{1-2\lambda}\log\Big(\frac{1-\lambda}{\lambda}\Big). |  | (38) |

Thus, for small λ\lambda, note that C⁡(λ)≈log⁡(1/λ)=−log⁡(λ)C(\lambda)\approx\log(1/\lambda)=-\log(\lambda).
For k≪−log⁡(λ)k\ll-\log(\lambda), the 1/k1/k formula is valid. However, near k≈−log⁡(λ)k\approx-\log(\lambda), the leading term −log(λ)/k-\log(\lambda)/k becomes of order 1, and for k≫−log⁡(λ)k\gg-\log(\lambda), the success rate is now very close to 1. Consequently, we see that if λ\lambda is very small, there is a soft cutoff scale around k≈−log⁡(λ)k\approx-\log(\lambda).

### E.7 Any Continuous Distribution with p⁡(passi​@​1)=c>0p(\operatorname{pass_{i}@1})=c>0

Suppose that the distribution over passi​@​1\operatorname{pass_{i}@1} is continuous and has constant non-zero density near 00:

|  |  |  |  |
| --- | --- | --- | --- |
|  | f⁡(0)=c>0f(0)=c>0 |  | (39) |

Because the density is continuous at 00 with f⁡(0)=c>0f(0)=c>0, there exist some δ>0\delta>0 such that:

|  |  |  |  |
| --- | --- | --- | --- |
|  | f⁡(p)=c+O⁡(p) for all ​p∈[0,δ].f(p)=c+O(p)\quad\quad\text{ for all }p\in[0,\delta]. |  | (40) |

Because the small passi​@​1\operatorname{pass_{i}@1} region dominates for large kk, a similar argument to the Kumaraswamy argument and Continuous Bernoulli argument yields power law scaling with respect to kk with exponent −1-1:

|  |  |  |  |
| --- | --- | --- | --- |
|  | −log⁡(pass𝒟​@​k)=c​k−1+o⁡(k−1).-\log\Big(\operatorname{pass_{\mathcal{D}}@k}\Big)=c\,k^{-1}+o(k^{-1}). |  | (41) |

This result is consistent with the Continuous Bernoulli, where cc is given by fContinuousBernoulli⁡(λ)​(0,λ)=C⁡(λ)​(1−λ)f_{\operatorname{ContinuousBernoulli(\lambda)}}(0;\lambda)=C(\lambda)(1-\lambda) for λ<1/2\lambda<1/2. This result reveals that the Continous Bernoulli is just one instance of a larger family: any continuous distribution with non-zero constant density at passi​@​1=0\operatorname{pass_{i}@1}=0 will exhibit power law scaling with exponent −1-1.

### E.8 Reciprocal Distribution: passi​@​1∼Reciprocal⁡(a,b)\operatorname{pass_{i}@1}\sim\operatorname{Reciprocal}(a,b)

Next, suppose the model’s passi​@​1∼Reciprocal⁡(a,b)\operatorname{pass_{i}@1}\sim\operatorname{Reciprocal(a,b)} distribution with 0<a<b<10<a<b<1. The probability density function of this distribution over the support x∈[a,b]x\in[a,b] is:

|  |  |  |  |
| --- | --- | --- | --- |
|  | f⁡(x,a,b)=1(log⁡(b)−log⁡(a))​xf(x;a,b)=\frac{1}{(\log(b)-\log(a))\,x} |  | (42) |

As with the other distributions, the aggregate success rate after kk attempts is:

|  |  |  |
| --- | --- | --- |
|  | passReciprocal⁡(a,b)​@​k=𝔼⁡[passi​@​k]= 1−Ik,whereIk​=def​∫x=ab(1−x)k​1(log⁡b−log⁡a)​x​dx.\operatorname{pass_{\mathrm{Reciprocal}(a,b)}@k}\;=\;\mathbb{E}\bigl[\operatorname{pass_{i}@k}\bigr]\;=\;1\;-\;I_{k},\quad\text{where}\quad I_{k}\;\defeq\;\int_{x=a}^{b}(1-x)^{k}\,\frac{1}{(\log b-\log a)\,x}\,\mathrm{d}x. |  |

We aim to show that IkI_{k} is on the order of
(1−a)kk\frac{(1-a)^{k}}{k}. The main contribution to the integral arises from the vicinity of x=ax=a, because (1−x)k(1-x)^{k} decays rapidly as xx grows away from aa.

Step 1: Change of variable.
Define y​=defx−ay\defeq x-a, so the domain x∈[a,b]x\in[a,b] becomes y∈[0,b−a]y\in[0,b-a]. Then

|  |  |  |
| --- | --- | --- |
|  | (1−x)k=((1−a)−y)k,(1-x)^{k}\;=\;\bigl((1-a)-y\bigr)^{k}, |  |

and

|  |  |  |
| --- | --- | --- |
|  | Ik=1log⁡(b/a)​∫y=0b−a((1−a)−y)k​1a+y​𝑑y.I_{k}\;=\;\frac{1}{\log(b/a)}\int_{y=0}^{\,b-a}\bigl((1-a)-y\bigr)^{k}\;\frac{1}{a+y}\,\mathrm{d}y. |  |

Step 2: Expansion near y=0y=0.
For small yy, write (1−a)−y=(1−a)​(1−y1−a)(1-a)-y=(1-a)\bigl(1-\tfrac{y}{1-a}\bigr); hence

|  |  |  |
| --- | --- | --- |
|  | log⁡((1−a)−y)=log⁡(1−a)+log⁡(1−y 1−a).\log\bigl((1-a)-y\bigr)\;=\;\log(1-a)\;+\;\log\Bigl(1-\tfrac{y}{\,1-a\,}\Bigr). |  |

Using log⁡(1−z)=−z+O⁡(z2)\log(1-z)=-z+O(z^{2}) for small zz, we get

|  |  |  |
| --- | --- | --- |
|  | log⁡((1−a)−y)=log⁡(1−a)−y1−a+O⁡(y2(1−a)2),\log\bigl((1-a)-y\bigr)\;=\;\log(1-a)\;-\;\frac{y}{1-a}\;+\;O\bigl(\tfrac{y^{2}}{(1-a)^{2}}\bigr), |  |

so

|  |  |  |
| --- | --- | --- |
|  | (1−a−y)k=exp⁡(k​log⁡(1−a)−k​y 1−a+O⁡(k​y2(1−a)2)).(1-a-y)^{k}\;=\;\exp\Bigl(k\,\log(1-a)\;-\;k\,\tfrac{y}{\,1-a\,}\;+\;O\bigl(\tfrac{k\,y^{2}}{(1-a)^{2}}\bigr)\Bigr). |  |

In particular, for yy up to c/kc/k, the term k​y2=O⁡(1)k\,y^{2}=O(1) remains bounded, so

|  |  |  |
| --- | --- | --- |
|  | (1−a−y)k=(1−a)k​exp⁡(−k​y 1−a)​[ 1+O⁡(1k)].(1-a-y)^{k}\;=\;(1-a)^{k}\,\exp\Bigl(-\tfrac{k\,y}{\,1-a\,}\Bigr)\bigl[\,1+O\bigl(\tfrac{1}{k}\bigr)\bigr]. |  |

Step 3: The integral is dominated by y∈[0,O⁡(1k)]y\in[0,O(\tfrac{1}{k})].
For large kk, exp⁡(−k​y 1−a)\exp\bigl(-\tfrac{k\,y}{\,1-a\,}\bigr) decays quickly once yy exceeds a multiple of 1−ak\tfrac{1-a}{k}. Consequently, the integral from y=c0/ky=c_{0}/k to b−ab-a is exponentially small in kk. On [0,c0/k][0,c_{0}/k], we also have (a+y)−1=1a+O⁡(1k)(a+y)^{-1}=\frac{1}{a}+O\bigl(\tfrac{1}{k}\bigr). Thus

|  |  |  |
| --- | --- | --- |
|  | Ik=1log⁡(b/a)​∫y=0c0/k(1−a−y)k​1a+y​𝑑y+(exponentially small tail).I_{k}\;=\;\frac{1}{\log(b/a)}\int_{y=0}^{c_{0}/k}(1-a-y)^{k}\;\frac{1}{a+y}\,\mathrm{d}y\;+\;\text{(exponentially small tail)}. |  |

Substitute our approximation from Step 2 into the integrand:

|  |  |  |
| --- | --- | --- |
|  | (1−a−y)k​1a+y=(1−a)k​exp⁡(−k​y 1−a)​[1a+O⁡(1k)].(1-a-y)^{k}\,\frac{1}{a+y}\;=\;(1-a)^{k}\,\exp\Bigl(-\tfrac{k\,y}{\,1-a\,}\Bigr)\;\Bigl[\tfrac{1}{a}+O\bigl(\tfrac{1}{k}\bigr)\Bigr]. |  |

Step 4: Change variable u=k​y1−au=\frac{k\,y}{1-a}.
Then y=(1−a)​uky=\frac{(1-a)\,u}{k} and d​y=1−ak​d​u\mathrm{d}y=\frac{1-a}{k}\,\mathrm{d}u. The upper limit y=c0/ky=c_{0}/k corresponds to u=c0​(1−a1)u=c_{0}\,\bigl(\tfrac{1-a}{1}\bigr), so

|  |  |  |
| --- | --- | --- |
|  | ∫y=0c0/kexp⁡(−k​y 1−a)​𝑑y=∫u=0c0​(1−a)e−u​1−ak​𝑑u.\int_{y=0}^{c_{0}/k}\exp\Bigl(-\tfrac{k\,y}{\,1-a\,}\Bigr)\,\mathrm{d}y\;=\;\int_{u=0}^{c_{0}\,(1-a)}e^{-u}\;\frac{1-a}{k}\,\mathrm{d}u. |  |

Letting c0→∞c_{0}\to\infty only contributes an e−c0​(1−a)e^{-c_{0}(1-a)} factor to the tail, which vanishes. Hence

|  |  |  |
| --- | --- | --- |
|  | ∫y=0∞exp⁡(−k​y 1−a)​𝑑y=1−ak​∫u=0∞e−u​𝑑u=1−ak.\int_{y=0}^{\infty}\exp\Bigl(-\tfrac{k\,y}{\,1-a\,}\Bigr)\,\mathrm{d}y\;=\;\frac{1-a}{\,k\,}\int_{u=0}^{\infty}e^{-u}\,\mathrm{d}u\;=\;\frac{1-a}{k}. |  |

Putting all factors together,

|  |  |  |
| --- | --- | --- |
|  | Ik=1log⁡(b/a)​(1−a)k​[1a+O⁡(1k)]​1−ak+(exponentially small in k).I_{k}\;=\;\frac{1}{\log(b/a)}\;(1-a)^{k}\;\Bigl[\tfrac{1}{a}+O\bigl(\tfrac{1}{k}\bigr)\Bigr]\;\frac{1-a}{k}\;+\;\text{(exponentially small in $k$)}. |  |

Thus in big-Theta form,

|  |  |  |
| --- | --- | --- |
|  | Ik=Θ⁡((1−a)kk).I_{k}\;=\;\Theta\Bigl(\tfrac{(1-a)^{k}}{k}\Bigr). |  |

Conclusion.
Since
passReciprocal⁡(a,b)​@​k=1−Ik,\operatorname{pass_{\mathrm{Reciprocal}(a,b)}@k}=1-I_{k},
we get

|  |  |  |
| --- | --- | --- |
|  | passReciprocal⁡(a,b)​@​k= 1−Θ⁡((1−a)kk).\operatorname{pass_{\mathrm{Reciprocal}(a,b)}@k}\;=\;1\;-\;\Theta\Bigl(\tfrac{(1-a)^{k}}{k}\Bigr). |  |

Moreover, using −log⁡(1−y)=y+O⁡(y2)-\log(1-y)=y+O(y^{2}) for small yy, it follows that

|  |  |  |
| --- | --- | --- |
|  | −log⁡(passReciprocal⁡(a,b)​@​k)=Θ⁡((1−a)kk).-\log\Bigl(\operatorname{pass_{\mathrm{Reciprocal}(a,b)}@k}\Bigr)\;=\;\Theta\Bigl(\tfrac{(1-a)^{k}}{k}\Bigr). |  |

Hence the negative log aggregate success rate converges to 11 *exponentially fast* in kk, which is *not* a power law in kk.

### Sufficient Condition for Power-Law Scaling in Negative Log of Aggregate Success

###### Theorem E.1.

Let 𝒟\mathcal{D} be a probability distribution on [0,1][0,1] with PDF f⁡(p)f(p).
Suppose there exist constants b>0b>0, C>0C>0, θ>0\theta>0 and δ>0\delta>0 such that,
for all 0<p<δ0<p<\delta, we have

|  |  |  |
| --- | --- | --- |
|  | f⁡(p)=C​pb−1+O⁡(pb−1+θ).f(p)\;=\;C\,p^{\,b-1}\;+\;O\bigl(p^{\,b-1+\theta}\bigr). |  |

Then, for large kk,

|  |  |  |
| --- | --- | --- |
|  | 1−pass𝒟​@​k=C​Γ​(b)​k−b+O⁡(k−b−min⁡( 1,θ)),1\;-\;\operatorname{pass_{\mathcal{D}}@k}\;=\;C\,\Gamma(b)\,k^{-b}\;+\;O\bigl(k^{-b-\min(\,1,\theta)}\bigr), |  |

which implies

|  |  |  |
| --- | --- | --- |
|  | −log⁡(pass𝒟​@​k)=C​Γ​(b)​k−b+o⁡(k−b).-\log\Bigl(\operatorname{pass_{\mathcal{D}}@k}\Bigr)\;=\;C\,\Gamma(b)\,k^{-b}\;+\;o\bigl(k^{-b}\bigr). |  |

Equivalently, including the leading constant),

|  |  |  |
| --- | --- | --- |
|  | −log⁡(pass𝒟​@​k)∼C​Γ​(b)​k−b.-\log\bigl(\operatorname{pass_{\mathcal{D}}@k}\bigr)\;\sim\;C\,\Gamma(b)\;k^{-b}. |  |

###### Proof.

Step 1. Decompose the key integral.
  
Define

|  |  |  |
| --- | --- | --- |
|  | Ik​=def 1−pass𝒟​@​k=∫01(1−p)k​f​(p)​dp.I_{k}\;\defeq\;1\;-\;\operatorname{pass_{\mathcal{D}}@k}\;=\;\int_{0}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p. |  |

For a positive constant c>0c>0, split IkI_{k}:

|  |  |  |
| --- | --- | --- |
|  | Ik=∫ 0c/k(1−p)k​f​(p)​𝑑p+∫c/k 1(1−p)k​f​(p)​𝑑p​=defIk,left+Ik,right.I_{k}\;=\;\int_{\,0}^{\,c/k}(1-p)^{k}\,f(p)\,\mathrm{d}p\;\;+\;\;\int_{\,c/k}^{\,1}(1-p)^{k}\,f(p)\,\mathrm{d}p\;\;\defeq\;\;I_{k,\mathrm{left}}\;+\;I_{k,\mathrm{right}}. |  |

#### Right Tail Bound (Ik,rightI_{k,\mathrm{right}}).

For p≥c/kp\geq c/k, observe (1−p)k≤e−k​p≤e−c(1-p)^{k}\leq e^{-k\,p}\leq e^{-c}. Hence

|  |  |  |
| --- | --- | --- |
|  | Ik,right=∫c/k1(1−p)k​f​(p)​𝑑p≤e−c​∫01f⁡(p)​𝑑p=e−c.I_{k,\mathrm{right}}\;=\;\int_{c/k}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p\;\leq\;e^{-c}\,\int_{0}^{1}f(p)\,\mathrm{d}p\;=\;e^{-c}. |  |

Since cc can be made arbitrarily large, e−ce^{-c} can be driven below *any* power of 1/k1/k.
Thus Ik,right=o⁡(k−α)I_{k,\mathrm{right}}=o\bigl(k^{-\alpha}\bigr) for any α>0\alpha>0.
We may therefore focus on

|  |  |  |
| --- | --- | --- |
|  | Ik,left=∫ 0c/k(1−p)k​f​(p)​𝑑p,I_{k,\mathrm{left}}\;=\;\int_{\,0}^{\,c/k}(1-p)^{k}\,f(p)\,\mathrm{d}p, |  |

knowing that Ik,rightI_{k,\mathrm{right}} is negligible in polynomial-type estimates.

Step 2. Use the assumed behavior of f⁡(p)f(p) near p=0p=0.
  
By hypothesis, for pp up to some δ>0\delta>0,

|  |  |  |
| --- | --- | --- |
|  | f⁡(p)=C​pb−1+O⁡(pb−1+θ).f(p)\;=\;C\,p^{\,b-1}+O\bigl(p^{\,b-1+\theta}\bigr). |  |

Choose c/k<δc/k<\delta, so p≤c/k<δp\leq c/k<\delta for pp in the left integral. Then

|  |  |  |
| --- | --- | --- |
|  | Ik,left=∫ 0c/k(1−p)k​[C​pb−1+O⁡(pb−1+θ)]​𝑑p.I_{k,\mathrm{left}}\;=\;\int_{\,0}^{\,c/k}(1-p)^{k}\Bigl[\,C\,p^{\,b-1}+O\bigl(p^{\,b-1+\theta}\bigr)\Bigr]\,\mathrm{d}p. |  |

Split it into main term and error term:

|  |  |  |
| --- | --- | --- |
|  | Ik,left=C​∫ 0c/k(1−p)k​pb−1​𝑑p+∫ 0c/k(1−p)k​O​(pb−1+θ)​𝑑p.I_{k,\mathrm{left}}\;=\;C\,\int_{\,0}^{\,c/k}(1-p)^{k}\,p^{\,b-1}\,\mathrm{d}p\;+\;\int_{\,0}^{\,c/k}(1-p)^{k}\,O\bigl(p^{\,b-1+\theta}\bigr)\,\mathrm{d}p. |  |

Denote these TmainT_{\mathrm{main}} and TerrT_{\mathrm{err}}, respectively.

Step 3. Approximate (1−p)k(1-p)^{k} by e−k​pe^{-kp} and control the error.
  
For pp in [0,c/k][0,c/k], expand log⁡(1−p)=−p+O⁡(p2)\log(1-p)=-p+O(p^{2}). Thus

|  |  |  |
| --- | --- | --- |
|  | (1−p)k=exp⁡(k​log⁡(1−p))=e−k​p​exp⁡(O⁡(k​p2))=e−k​p​[ 1+O⁡(k​p2)].(1-p)^{k}\;=\;\exp\bigl(k\log(1-p)\bigr)\;=\;e^{-k\,p}\,\exp\bigl(O(k\,p^{2})\bigr)\;=\;e^{-k\,p}\,\bigl[\,1+O(k\,p^{2})\bigr]. |  |

Since p≤c/kp\leq c/k, we get k​p2≤c2/kk\,p^{2}\leq c^{2}/k, which is bounded for large kk. Consequently,

|  |  |  |
| --- | --- | --- |
|  | (1−p)k=e−k​p+O⁡(k​p2​e−k​p).(1-p)^{k}=e^{-k\,p}+O\bigl(k\,p^{2}\,e^{-k\,p}\bigr). |  |

We will use this in both TmainT_{\mathrm{main}} and TerrT_{\mathrm{err}}.

Step 4. Main term TmainT_{\mathrm{main}}.

|  |  |  |
| --- | --- | --- |
|  | Tmain=C​∫ 0c/k(1−p)k​pb−1​𝑑p.T_{\mathrm{main}}\;=\;C\int_{\,0}^{\,c/k}(1-p)^{k}\,p^{\,b-1}\,\mathrm{d}p. |  |

Substituting (1−p)k=e−k​p+O⁡(k​p2​e−k​p)(1-p)^{k}=e^{-k\,p}+O\bigl(k\,p^{2}\,e^{-k\,p}\bigr),

|  |  |  |
| --- | --- | --- |
|  | Tmain=C​∫ 0c/ke−k​p​pb−1​𝑑p+C​∫ 0c/kO⁡(k​pb+1​e−k​p)​𝑑p.T_{\mathrm{main}}\;=\;C\int_{\,0}^{\,c/k}e^{-k\,p}\,p^{\,b-1}\,\mathrm{d}p\;+\;C\int_{\,0}^{\,c/k}O\bigl(k\,p^{\,b+1}\,e^{-k\,p}\bigr)\,\mathrm{d}p. |  |

Call these two integrals T1T_{1} and T2T_{2}.

#### T1T_{1} term.

|  |  |  |
| --- | --- | --- |
|  | T1=C​∫ 0c/kpb−1​e−k​p​𝑑p.T_{1}=C\int_{\,0}^{\,c/k}p^{\,b-1}\,e^{-k\,p}\,\mathrm{d}p. |  |

Make the substitution u​=defk​pu\defeq k\,p. Then p=u/kp=u/k, d​p=d​u/k\mathrm{d}p=\mathrm{d}u/k, and pb−1=k−b+1​ub−1p^{\,b-1}=k^{-b+1}\,u^{\,b-1}.
The upper limit p=c/kp=c/k becomes u=cu=c. Thus

|  |  |  |
| --- | --- | --- |
|  | T1=C​∫ 0c(uk)b−1​e−u​d​uk=C​k−b​∫ 0cub−1​e−u​𝑑u.T_{1}=C\int_{\,0}^{\,c}\bigl(\tfrac{u}{k}\bigr)^{b-1}\,e^{-u}\,\tfrac{\mathrm{d}u}{k}=C\,k^{-b}\int_{\,0}^{\,c}u^{\,b-1}\,e^{-u}\,\mathrm{d}u. |  |

As c→∞c\to\infty, ∫0cub−1​e−u​𝑑u→Γ⁡(b)\int_{0}^{c}u^{\,b-1}e^{-u}\,\mathrm{d}u\to\Gamma(b).
So

|  |  |  |
| --- | --- | --- |
|  | T1=C​k−b​(Γ⁡(b)−Rc),where ​|Rc|=O⁡(e−c).T_{1}=C\,k^{-b}\Bigl(\Gamma(b)-R_{c}\Bigr),\quad\text{where }|R_{c}|=O\bigl(e^{-c}\bigr). |  |

By choosing cc large after k→∞k\to\infty, we conclude

|  |  |  |
| --- | --- | --- |
|  | T1=C​Γ​(b)​k−b+o⁡(k−b).T_{1}=C\,\Gamma(b)\,k^{-b}+o\bigl(k^{-b}\bigr). |  |

#### T2T_{2} term.

|  |  |  |
| --- | --- | --- |
|  | T2=C​∫ 0c/kO⁡(k​pb+1​e−k​p)​𝑑p.T_{2}=C\int_{\,0}^{\,c/k}O\bigl(k\,p^{\,b+1}\,e^{-k\,p}\bigr)\,\mathrm{d}p. |  |

Inside the integral, k​pb+1​e−k​pk\,p^{\,b+1}\,e^{-k\,p} is the main factor. Substituting u​=defk​pu\defeq k\,p again,

|  |  |  |
| --- | --- | --- |
|  | pb+1=(uk)b+1=k−b−1​ub+1.p^{\,b+1}=\bigl(\tfrac{u}{k}\bigr)^{b+1}=k^{-b-1}\,u^{\,b+1}. |  |

Hence

|  |  |  |
| --- | --- | --- |
|  | T2=C​O​(1)​∫ 0c/kk​pb+1​e−k​p​𝑑p=O⁡(k)​∫ 0c/kpb+1​e−k​p​𝑑p.T_{2}=C\,O(1)\,\int_{\,0}^{\,c/k}k\,p^{\,b+1}\,e^{-k\,p}\,\mathrm{d}p=O(k)\,\int_{\,0}^{\,c/k}p^{\,b+1}e^{-k\,p}\,\mathrm{d}p. |  |

Substitute u=k​pu=k\,p and d​p=d​u/k\mathrm{d}p=\mathrm{d}u/k. Then

|  |  |  |
| --- | --- | --- |
|  | T2=O⁡(k)​∫ 0c(uk)b+1​e−u​d​uk=O⁡(k)​k−b−2​∫ 0cub+1​e−u​𝑑u=O⁡(k−b−1).T_{2}=O(k)\,\int_{\,0}^{\,c}\bigl(\tfrac{u}{k}\bigr)^{b+1}e^{-u}\,\tfrac{\mathrm{d}u}{\,k\,}=O(k)\,k^{-b-2}\int_{\,0}^{\,c}u^{\,b+1}\,e^{-u}\,\mathrm{d}u=O\bigl(k^{-b-1}\bigr). |  |

Thus T2T_{2} is of strictly smaller order than k−bk^{-b}.

Combine T1T_{1} and T2T_{2}:

|  |  |  |
| --- | --- | --- |
|  | Tmain=C​Γ​(b)​k−b+O⁡(k−b−1).T_{\mathrm{main}}=C\,\Gamma(b)\,k^{-b}+O\bigl(k^{-b-1}\bigr). |  |

Step 5. Error term TerrT_{\mathrm{err}}.
  
Recall

|  |  |  |
| --- | --- | --- |
|  | Terr=∫ 0c/k(1−p)k​O​(pb−1+θ)​𝑑p.T_{\mathrm{err}}=\int_{\,0}^{\,c/k}(1-p)^{k}\,O\bigl(p^{\,b-1+\theta}\bigr)\,\mathrm{d}p. |  |

Exactly the same substitution (1−p)k=e−k​p+O⁡(k​p2​e−k​p)(1-p)^{k}=e^{-kp}+O(k\,p^{2}\,e^{-k\,p}) plus u=k​pu=k\,p shows

|  |  |  |
| --- | --- | --- |
|  | Terr=O⁡(∫ 0c/kpb−1+θ​e−k​p​𝑑p)+O⁡(∫ 0c/kk​pb+1+θ​e−k​p​𝑑p).T_{\mathrm{err}}=O\Bigl(\int_{\,0}^{\,c/k}p^{\,b-1+\theta}\,e^{-k\,p}\,\mathrm{d}p\Bigr)\;+\;O\Bigl(\int_{\,0}^{\,c/k}k\,p^{\,b+1+\theta}\,e^{-k\,p}\,\mathrm{d}p\Bigr). |  |

When substituting u=k​pu=k\,p, the exponent on pp increases by +1+1 each time if we multiply by kk, so each term is of order k−b−θk^{-b-\theta} or smaller. Concretely,

|  |  |  |
| --- | --- | --- |
|  | ∫0c/kpb−1+θ​e−k​p​𝑑p=k−b−θ​∫0cub−1+θ​e−u​𝑑u=O⁡(k−b−θ),\int_{0}^{c/k}p^{\,b-1+\theta}\,e^{-k\,p}\,\mathrm{d}p=k^{-b-\theta}\,\int_{0}^{c}u^{\,b-1+\theta}\,e^{-u}\,\mathrm{d}u=O\bigl(k^{-b-\theta}\bigr), |  |

and similarly for the second term, which is even smaller.
Hence

|  |  |  |
| --- | --- | --- |
|  | Terr=O⁡(k−b−θ).T_{\mathrm{err}}=O\bigl(k^{-b-\theta}\bigr). |  |

Step 6. Putting it all together.
  
Summarize:

|  |  |  |
| --- | --- | --- |
|  | Ik,left=Tmain+Terr=C​Γ​(b)​k−b+O⁡(k−b−1)+O⁡(k−b−θ).I_{k,\mathrm{left}}=T_{\mathrm{main}}+T_{\mathrm{err}}=C\,\Gamma(b)\,k^{-b}\;+\;O\bigl(k^{-b-1}\bigr)\;+\;O\bigl(k^{-b-\theta}\bigr). |  |

Thus

|  |  |  |
| --- | --- | --- |
|  | Ik,left=C​Γ​(b)​k−b+O⁡(k−b−min⁡(1,θ)).I_{k,\mathrm{left}}=C\,\Gamma(b)\,k^{-b}\;+\;O\bigl(k^{-b-\min(1,\theta)}\bigr). |  |

Recalling the tail piece Ik,right=e−c=o⁡(k−α)I_{k,\mathrm{right}}=e^{-c}=o\bigl(k^{-\alpha}\bigr) for any α\alpha, we obtain

|  |  |  |
| --- | --- | --- |
|  | Ik=Ik,left+Ik,right=C​Γ​(b)​k−b+O⁡(k−b−min⁡(1,θ)).I_{k}=I_{k,\mathrm{left}}+I_{k,\mathrm{right}}=C\,\Gamma(b)\,k^{-b}\;+\;O\bigl(k^{-b-\min(1,\theta)}\bigr). |  |

Hence

|  |  |  |
| --- | --- | --- |
|  | 1−pass𝒟​@​k=Ik∼C​Γ​(b)​k−b.1-\operatorname{pass_{\mathcal{D}}@k}=I_{k}\;\;\sim\;\;C\,\Gamma(b)\,k^{-b}. |  |

#### Final negative-log argument.

Since

|  |  |  |
| --- | --- | --- |
|  | pass𝒟​@​k=1−Ik=1−(C​Γ​(b)​k−b+O⁡(k−b−min⁡(1,θ))),\operatorname{pass_{\mathcal{D}}@k}=1-I_{k}=1-\bigl(C\,\Gamma(b)\,k^{-b}+O\bigl(k^{-b-\min(1,\theta)}\bigr)\bigr), |  |

for large kk it is very close to 1. Then

|  |  |  |
| --- | --- | --- |
|  | −log⁡(pass𝒟​@​k)=−log⁡(1−C​Γ​(b)​k−b+⋯).-\log\Bigl(\operatorname{pass_{\mathcal{D}}@k}\Bigr)=-\log\Bigl(1-C\,\Gamma(b)\,k^{-b}+\cdots\Bigr). |  |

Using the expansion −log⁡(1−x)=x+O⁡(x2)-\log(1-x)=x+O(x^{2}) as x→0x\to 0, and here x=C​Γ​(b)​k−bx=C\,\Gamma(b)\,k^{-b}, we get

|  |  |  |
| --- | --- | --- |
|  | −log⁡(pass𝒟​@​k)=C​Γ​(b)​k−b+o⁡(k−b).-\log\Bigl(\operatorname{pass_{\mathcal{D}}@k}\Bigr)=C\,\Gamma(b)\,k^{-b}+o\bigl(k^{-b}\bigr). |  |

In the “∼\sim” notation including the leading coefficient:

|  |  |  |
| --- | --- | --- |
|  | −log⁡(pass𝒟​@​k)∼C​Γ​(b)​k−b.-\log\Bigl(\operatorname{pass_{\mathcal{D}}@k}\Bigr)\;\sim\;C\,\Gamma(b)\;k^{-b}. |  |

This completes the proof.
∎

### E.9 Necessary Condition for Power Law Scaling from Distribution over passi​@​1\operatorname{pass_{i}@1}

###### Theorem E.2.

Let 𝒟\mathcal{D} be a probability distribution over [0,1][0,1] with a PDF f⁡(p)f(p) satisfying the following regularity near p=0p=0:

- •

  No point mass at p=0p=0. So ∫01f⁡(p)​𝑑p=1\int_{0}^{1}f(p)\,\mathrm{d}p=1, and ff is a genuine PDF on (0,1](0,1].
- •

  Continuity and nonnegative behavior near p=0p=0. There exist δ>0\delta>0 such that ff is continuous on [0,δ][0,\delta] and has no pathological oscillations or singularities that violate integrability.

Define the aggregate success rate at kk attempts:

|  |  |  |
| --- | --- | --- |
|  | pass𝒟​@​k⁡=def​∫01[ 1−(1−p)k]​f​(p)​dp\operatorname{pass_{\mathcal{D}}@k}\;\defeq\;\int_{0}^{1}\Bigl[\,1-(1-p)^{k}\Bigr]\,f(p)\,\mathrm{d}p |  |

and relatedly

|  |  |  |
| --- | --- | --- |
|  | Ik​=def​∫01(1−p)k​f​(p)​dp= 1−pass𝒟​@​k.I_{k}\;\;\defeq\;\;\int_{0}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p\;=\;1-\operatorname{pass_{\mathcal{D}}@k}. |  |

Assume that there exist constants A>0A>0 and b>0b>0 such that for large kk:

|  |  |  |
| --- | --- | --- |
|  | −log⁡(pass𝒟​@​k)∼A​k−b-\log\bigl(\operatorname{pass_{\mathcal{D}}@k}\bigr)\;\;\sim\;\;A\,k^{-b} |  |

Then

|  |  |  |
| --- | --- | --- |
|  | Ik=A​k−b+o⁡(k−b),I_{k}\;=\;A\,k^{-b}+o\bigl(k^{-b}\bigr), |  |

and under the mild regularity assumptions above,

|  |  |  |
| --- | --- | --- |
|  | f⁡(p)∼AΓ⁡(b)​pb−1as ​p→0+.f(p)\;\;\sim\;\;\frac{A}{\,\Gamma(b)\,}\;p^{\,b-1}\quad\text{as }p\to 0^{+}. |  |

###### Proof.

Step 1. Relating IkI_{k} to −log⁡(pass𝒟​@​k)-\log(\operatorname{pass_{\mathcal{D}}@k}).

By definition,

|  |  |  |
| --- | --- | --- |
|  | pass𝒟​@​k= 1−Ik,Ik=∫01(1−p)k​f​(p)​𝑑p.\operatorname{pass_{\mathcal{D}}@k}\;=\;1-I_{k},\quad I_{k}\;=\;\int_{0}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p. |  |

Since

|  |  |  |
| --- | --- | --- |
|  | −log⁡(pass𝒟​@​k)∼A​k−b,-\log\Bigl(\operatorname{pass_{\mathcal{D}}@k}\Bigr)\;\;\sim\;\;A\,k^{-b}, |  |

we have, for large kk,

|  |  |  |
| --- | --- | --- |
|  | pass𝒟​@​k=exp⁡(−A​k−b​(1+o⁡(1))).\operatorname{pass_{\mathcal{D}}@k}\;=\;\exp\bigl(-A\,k^{-b}\,(1+o(1))\bigr). |  |

When xx is small, exp⁡(−x)=1−x+O⁡(x2)\exp(-x)=1-x+O(x^{2}). Thus

|  |  |  |
| --- | --- | --- |
|  | Ik= 1−pass𝒟​@​k=A​k−b+o⁡(k−b).I_{k}\;=\;1-\operatorname{pass_{\mathcal{D}}@k}\;=\;A\,k^{-b}+o\bigl(k^{-b}\bigr). |  |

So

|  |  |  |
| --- | --- | --- |
|  | Ik∼A​k−b.I_{k}\;\;\sim\;\;A\,k^{-b}. |  |

Step 2. Restricting to a small interval near p=0p=0.

Since (1−p)k(1-p)^{k} decays exponentially once pp is on the order of 1/k1/k or larger, we split:

|  |  |  |
| --- | --- | --- |
|  | Ik​=def​∫01(1−p)k​f​(p)​dp=∫0c/k(1−p)k​f​(p)​dp+∫c/k1(1−p)k​f​(p)​dp​=def​Ik,left+Ik,right,I_{k}\;\defeq\;\int_{0}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p\;=\;\int_{0}^{c/k}(1-p)^{k}\,f(p)\,\mathrm{d}p\;+\;\int_{c/k}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p\;\defeq\;I_{k,\mathrm{left}}+I_{k,\mathrm{right}}, |  |

for some positive constant cc. In the region p≥c/kp\geq c/k, we have (1−p)k≤e−k​p≤e−c(1-p)^{k}\leq e^{-k\,p}\leq e^{-c}, so

|  |  |  |
| --- | --- | --- |
|  | Ik,right≤e−c​∫01f⁡(p)​𝑑p=e−c.I_{k,\mathrm{right}}\;\leq\;e^{-c}\;\int_{0}^{1}f(p)\,\mathrm{d}p\;=\;e^{-c}. |  |

Since c>0c>0 can be made large, e−ce^{-c} can be driven below any fixed power of 1/k1/k.
Hence for the Θ⁡(k−b)\Theta(k^{-b}) behavior, the main contribution comes from [0,c/k][0,c/k].

Thus

|  |  |  |
| --- | --- | --- |
|  | Ik=Ik,left+o⁡(k−m)​for every ​m>0I_{k}\;=\;I_{k,\mathrm{left}}\;+\;o\bigl(k^{-m}\bigr)\;\;\text{for every }m>0 |  |

Step 3. Change of variables and controlling the ratio of (1−p)k(1-p)^{k} to e−k​pe^{-kp}.

(a) Ratio to e−k​pe^{-kp}.
For p∈[0,ck]p\in\bigl[0,\tfrac{c}{k}\bigr], define the ratio

|  |  |  |
| --- | --- | --- |
|  | Rk​(p)​=def(1−p)ke−k​p.R_{k}(p)\;\;\defeq\;\;\frac{(1-p)^{k}}{\,e^{-k\,p}\,}. |  |

We will show that Rk​(p)R_{k}(p) stays close to 11 uniformly in p∈[0,c/k]p\in[0,c/k] for large kk.
Indeed,

|  |  |  |
| --- | --- | --- |
|  | (1−p)k=exp⁡[k​log⁡(1−p)],log⁡(1−p)=−p−p22−p33−….(1-p)^{k}\;=\;\exp\Bigl[k\,\log(1-p)\Bigr],\quad\log(1-p)\;=\;-\,p\;-\;\frac{p^{2}}{2}\;-\;\frac{p^{3}}{3}\;-\;\dots\,. |  |

Hence

|  |  |  |
| --- | --- | --- |
|  | log⁡(1−p)+p=−p22−p33−…=O⁡(p2)as ​p→0.\log(1-p)+p\;=\;-\frac{p^{2}}{2}\;-\;\frac{p^{3}}{3}\;-\;\dots\;\;=\;\;O\bigl(p^{2}\bigr)\quad\text{as }p\to 0. |  |

Multiplying by kk, we get

|  |  |  |
| --- | --- | --- |
|  | k⁡[log⁡(1−p)+p]=O⁡(k​p2).k\,\bigl[\log(1-p)+p\bigr]\;=\;O\bigl(k\,p^{2}\bigr). |  |

Since 0≤p≤ck0\leq p\leq\tfrac{c}{k} implies k​p2≤c2kk\,p^{2}\leq\tfrac{c^{2}}{k}, which →0\to 0 as k→∞k\to\infty,
it follows that

|  |  |  |
| --- | --- | --- |
|  | k​log⁡(1−p)=−k​p+O⁡(1k).k\,\log(1-p)\;=\;-k\,p+O\bigl(\tfrac{1}{k}\bigr). |  |

Exponentiating:

|  |  |  |
| --- | --- | --- |
|  | (1−p)k=e−k​p​exp⁡(O⁡(1k))=e−k​p​[ 1+O⁡(1k)].(1-p)^{k}\;=\;e^{-\,k\,p}\,\exp\Bigl(O\bigl(\tfrac{1}{k}\bigr)\Bigr)\;=\;e^{-\,k\,p}\Bigl[\,1+O\bigl(\tfrac{1}{k}\bigr)\Bigr]. |  |

Thus

|  |  |  |
| --- | --- | --- |
|  | Rk​(p)=(1−p)ke−k​p= 1+O⁡(1k),R_{k}(p)\;=\;\frac{(1-p)^{k}}{\,e^{-k\,p}\,}\;=\;1+O\bigl(\tfrac{1}{k}\bigr), |  |

with the O⁡(1k)O(\tfrac{1}{k}) bound uniform for all p∈[0,c/k]p\in[0,c/k]. In other words, there is some constant M>0M>0 (independent of kk) such that

|  |  |  |
| --- | --- | --- |
|  | |Rk​(p)−1|≤Mkfor all ​p∈[0,ck].\bigl|R_{k}(p)-1\bigr|\;\leq\;\frac{M}{k}\quad\text{for all }p\in\Bigl[0,\frac{c}{k}\Bigr]. |  |

(b) Integral expression using Rk​(p)R_{k}(p).
Hence on [0,c/k][0,c/k],

|  |  |  |
| --- | --- | --- |
|  | (1−p)k​f​(p)=e−k​p​Rk​(p)​f​(p).(1-p)^{k}\,f(p)\;=\;e^{-k\,p}\,R_{k}(p)\,f(p). |  |

Thus

|  |  |  |
| --- | --- | --- |
|  | Ik,left=∫0c/ke−k​p​f​(p)​Rk​(p)​𝑑p.I_{k,\mathrm{left}}\;=\;\int_{0}^{c/k}e^{-k\,p}\,f(p)\,R_{k}(p)\,\mathrm{d}p. |  |

Define Δk​(p)​=defRk​(p)−1\Delta_{k}(p)\defeq R_{k}(p)-1, which satisfies |Δk​(p)|≤M/k|\Delta_{k}(p)|\leq M/k. Then

|  |  |  |  |
| --- | --- | --- | --- |
|  | Ik,left=∫0c/ke−k​p​f​(p)​𝑑p+∫0c/ke−k​p​f​(p)​Δk​(p)​𝑑p.I_{k,\mathrm{left}}=\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p\;\;+\;\;\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\Delta_{k}(p)\,\mathrm{d}p. |  | (43) |

Step 4. Substitution u=k​pu=k\,p and deriving f⁡(p)∼pb−1f(p)\sim p^{\,b-1}.

(a) The leading part.
Focus on the first term of equation [43](#A5.E43 "Equation 43 ‣ Proof. ‣ E.9 Necessary Condition for Power Law Scaling from Distribution over pass_i⁢@⁢1 ‣ Appendix E Aggregate Power Laws from a Probability Distribution over Exponential Functions"):

|  |  |  |
| --- | --- | --- |
|  | ∫0c/ke−k​p​f​(p)​𝑑p.\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p. |  |

Substitute u​=defk​pu\defeq k\,p, so p=ukp=\tfrac{u}{k} and d​p=1k​d​u\mathrm{d}p=\tfrac{1}{k}\,\mathrm{d}u. The upper limit p=ckp=\tfrac{c}{k} becomes u=cu=c. Thus

|  |  |  |
| --- | --- | --- |
|  | ∫0c/ke−k​p​f​(p)​𝑑p=∫0ce−u​f​(uk)​d​uk.\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p=\int_{0}^{c}e^{-u}\,f\Bigl(\frac{u}{k}\Bigr)\,\frac{\mathrm{d}u}{\,k\,}. |  |

Hence

|  |  |  |
| --- | --- | --- |
|  | ∫0c/ke−k​p​f​(p)​𝑑p=1k​∫0ce−u​f​(uk)​𝑑u.\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p=\frac{1}{k}\,\int_{0}^{c}e^{-u}\,f\Bigl(\frac{u}{k}\Bigr)\,\mathrm{d}u. |  |

(b) The error part.
The second term in equation [43](#A5.E43 "Equation 43 ‣ Proof. ‣ E.9 Necessary Condition for Power Law Scaling from Distribution over pass_i⁢@⁢1 ‣ Appendix E Aggregate Power Laws from a Probability Distribution over Exponential Functions") has Δk​(p)=Rk​(p)−1\Delta_{k}(p)=R_{k}(p)-1 satisfying |Δk​(p)|≤Mk|\Delta_{k}(p)|\leq\frac{M}{k}. So

|  |  |  |
| --- | --- | --- |
|  | |∫0c/ke−k​p​f​(p)​Δk​(p)​𝑑p|≤Mk​∫0c/ke−k​p​f​(p)​𝑑p.\left|\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\Delta_{k}(p)\,\mathrm{d}p\right|\;\leq\;\frac{M}{\,k\,}\,\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p. |  |

But the integral ∫0c/ke−k​p​f​(p)​𝑑p\int_{0}^{c/k}e^{-k\,p}\,f(p)\,\mathrm{d}p is precisely the leading part we just considered. Thus the error is bounded by Mk\frac{M}{k} times a term that will turn out to be Θ⁡(k−b)\Theta(k^{-b}).
Hence the error is subleading if b<1b<1 is not the case—but even then, we can keep track of it systematically.

Overall, combining both terms, we get

|  |  |  |  |
| --- | --- | --- | --- |
|  | Ik,left=1k​∫0ce−u​f​(uk)​𝑑u+O⁡(1k⋅(leading integral)).I_{k,\mathrm{left}}\;=\;\frac{1}{k}\int_{0}^{c}e^{-u}\,f\Bigl(\frac{u}{k}\Bigr)\,\mathrm{d}u\;+\;O\bigl(\tfrac{1}{k}\cdot\text{(leading integral)}\bigr). |  | (44) |

(c) Matching Θ⁡(k−b)\Theta(k^{-b}).
Since Ik=Ik,left+Ik,rightI_{k}=I_{k,\mathrm{left}}+I_{k,\mathrm{right}} with Ik,rightI_{k,\mathrm{right}} negligible, we have

|  |  |  |
| --- | --- | --- |
|  | Ik=1k​∫0ce−u​f​(uk)​𝑑u+(small corrections).I_{k}\;=\;\frac{1}{k}\int_{0}^{c}e^{-u}\,f\Bigl(\tfrac{u}{k}\Bigr)\,\mathrm{d}u\;+\;\text{(small corrections)}. |  |

But by hypothesis, Ik∼α​k−bI_{k}\sim\alpha\,k^{-b}. Thus

|  |  |  |  |
| --- | --- | --- | --- |
|  | k⋅Ik=∫0ce−u​f​(uk)​𝑑u+(smaller terms)∼α​k1−b.k\cdot I_{k}\;=\;\int_{0}^{c}e^{-u}\,f\Bigl(\tfrac{u}{k}\Bigr)\,\mathrm{d}u\;+\;\text{(smaller terms)}\;\;\sim\;\;\alpha\,k^{1-b}. |  | (45) |

Hence the expression

|  |  |  |
| --- | --- | --- |
|  | ∫0ce−u​f​(uk)​𝑑u\int_{0}^{c}e^{-u}\,f\Bigl(\tfrac{u}{k}\Bigr)\,\mathrm{d}u |  |

must be Θ⁡(k 1−b)\Theta\bigl(k^{\,1-b}\bigr) for large kk. Since uk\tfrac{u}{k} is small for 0≤u≤c0\leq u\leq c, we are effectively sampling ff near 0. For the integral to produce k 1−bk^{\,1-b}, we deduce

|  |  |  |
| --- | --- | --- |
|  | f⁡(uk)=Θ⁡((uk)b−1),f\Bigl(\tfrac{u}{k}\Bigr)\;\;=\;\;\Theta\Bigl(\Bigl(\tfrac{u}{k}\Bigr)^{b-1}\Bigr), |  |

i.e. ff must behave like pb−1p^{\,b-1} near p=0p=0. Rewriting the constant in front, one obtains

|  |  |  |
| --- | --- | --- |
|  | f⁡(uk)=(uk)b−1​[some positive constant].f\Bigl(\tfrac{u}{k}\Bigr)\;=\;\Bigl(\tfrac{u}{k}\Bigr)^{b-1}\,\bigl[\text{some positive constant}\bigr]. |  |

(We then identify that constant with αΓ⁡(b)\frac{\alpha}{\Gamma(b)} by matching the integral precisely, just as in the prior argument.)

Step 5. Conclusion.
We have thus shown that over p∈[0,c/k]p\in[0,c/k], one has

|  |  |  |
| --- | --- | --- |
|  | (1−p)k=e−k​p​[ 1+O⁡(1k)],(1-p)^{k}\;=\;e^{-k\,p}\,\bigl[\,1+O(\tfrac{1}{k})\bigr], |  |

and upon integrating, the required k−bk^{-b} form for IkI_{k} forces

|  |  |  |
| --- | --- | --- |
|  | f⁡(p)=AΓ⁡(b)​pb−1+o⁡(pb−1),as ​p→0+.f(p)\;=\;\frac{A}{\Gamma(b)}\,p^{\,b-1}\;+\;o\bigl(p^{\,b-1}\bigr),\quad\text{as }p\to 0^{+}. |  |

This completes the necessity proof.

∎

Remark (Mild Regularity).
If ff had bizarre oscillations or nonintegrable singularities near 00, the integral ∫01(1−p)k​f​(p)​𝑑p\int_{0}^{1}(1-p)^{k}\,f(p)\,\mathrm{d}p might not produce a clean k−bk^{-b}. Typically, we impose monotonicity or at least continuity near p=0p=0, no atom at p=0p=0, and f⁡(0)=0f(0)=0 if b>1b>1 or f⁡(0)>0f(0)>0 if b=1b=1, etc. These assumptions exclude pathological behaviors and guarantee that the local shape of f⁡(p)f(p) drives a clean power law.

## Appendix F Maximum Likelihood Estimation of Scaled Beta-Binomial Distribution

To model the distribution of passi​@​1\operatorname{pass_{i}@1}, we can perform maximum likelihood estimation on a scaled three-parameter Beta-Binomial distribution, which we chose because each attempt on the ii-th problem is an i.i.d. Bernoulli random variable with success probability passi​@​1\operatorname{pass_{i}@1}, and we introduced a scale parameter because the largest passi​@​1\operatorname{pass_{i}@1} values were typically 1-2 orders of magnitude less than 1.0 (the maximum of the unscaled beta distribution’s support).

In greater detail, as background, the 4-parameter Beta distribution has PDF

|  |  |  |  |
| --- | --- | --- | --- |
|  | pY​(y,α,β,a,c)​=def(y−a)α−1​(c−y)β−1(c−a)α+β−1​B⁡(α,β),p_{Y}(y;\alpha,\beta,a,c)\defeq\frac{(y-a)^{\alpha-1}(c-y)^{\beta-1}}{(c-a)^{\alpha+\beta-1}\operatorname{B}(\alpha,\beta)}, |  | (46) |

where B⁡(⋅,⋅)\operatorname{B}(\cdot,\cdot) is the [Beta function](https://en.wikipedia.org/wiki/Beta_function). If the minimum aa is fixed at 00 and the maximum cc is constrained to a<c<1a<c<1, then the scaled three parameter Beta distribution simplifies to:

|  |  |  |  |
| --- | --- | --- | --- |
|  | fP​(p,α,β,a=0,c)=pα−1​(c−p)β−1cα+β−1​B⁡(α,β).f_{P}(p;\alpha,\beta,a=0,c)=\frac{p^{\alpha-1}(c-p)^{\beta-1}}{c^{\alpha+\beta-1}\operatorname{B}(\alpha,\beta)}. |  | (47) |

We want the PMF of a three-parameter Beta-Binomial distribution based on this scaled Beta distribution. For nn samples and xx successes, the PMF is:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | P⁡(X=x,α,β,c,n)\displaystyle P(X=x;\alpha,\beta,c,n) | =def∫0c(nx)px(1−p)n−xfP(p;α,β,a=0,c)dp\displaystyle\defeq\int_{0}^{c}\binom{n}{x}\,p^{x}\,(1-p)^{n-x}\,f_{P}(p;\alpha,\beta,a=0,c)\,dp |  | (48) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =(nx)​1cα+β−1​B⁡(α,β)​∫0cpx+α−1​(1−p)n−x​(c−p)β−1​𝑑p.\displaystyle=\binom{n}{x}\frac{1}{c^{\alpha+\beta-1}\operatorname{B}(\alpha,\beta)}\int_{0}^{c}p^{x+\alpha-1}\,(1-p)^{n-x}\,(c-p)^{\beta-1}\,dp. |  | (49) |

Using a change of variable p​=defc​zp\defeq c\,z, the PMF can be rewritten as

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | P⁡(X=x,α,β,c,n)\displaystyle P(X=x;\alpha,\beta,c,n) | =(nx)​cxB⁡(α,β)​∫01zx+α−1​(1−z)β−1​(1−c​z)n−x​𝑑z\displaystyle=\binom{n}{x}\frac{c^{x}}{\operatorname{B}(\alpha,\beta)}\int_{0}^{1}z^{x+\alpha-1}\,(1-z)^{\beta-1}\,(1-cz)^{n-x}\,dz |  | (50) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =(nx)cx​B​(x+α,β)B⁡(α,β)2F1(−(n−x),x+α;x+α+β;c),\displaystyle=\binom{n}{x}\;\frac{c^{x}\mathrm{B}\bigl(x+\alpha,\;\beta\bigr)}{\mathrm{B}(\alpha,\beta)}\mathchoice{\mathop{}\kern 4.48613pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}{\mathop{}\kern 4.48613pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}{\mathop{}\kern 3.90283pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}{\mathop{}\kern 3.90283pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}F_{1}\Bigl(-(n-x),\;x+\alpha;\;x+\alpha+\beta;\;c\Bigr), |  | (51) |

where 2F1(⋅,⋅;⋅;⋅)\mathchoice{\mathop{}\kern 4.48613pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}{\mathop{}\kern 4.48613pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}{\mathop{}\kern 3.90283pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}{\mathop{}\kern 3.90283pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}F_{1}(\cdot,\cdot;\cdot;\cdot) is the [(Gauss) hypergeometric function](https://en.wikipedia.org/wiki/Hypergeometric_function#Euler_type).

## Appendix G Maximum Likelihood Estimation of Scaled Kumaraswamy-Binomial Distribution

To model the distribution of passi​@​1\operatorname{pass_{i}@1}, we can perform maximum likelihood estimation on a scaled three-parameter Kumaraswamy-Binomial distribution, which we chose because each attempt on the ii-th problem is an i.i.d. Kumaraswamy random variable with success probability passi​@​1\operatorname{pass_{i}@1}, and we introduced a scale parameter because the largest passi​@​1\operatorname{pass_{i}@1} values were typically 1-2 orders of magnitude less than 1.0 (the maximum of the unscaled beta distribution’s support).

In greater detail, the scaled three parameter Kumaraswamy distribution simplifies to:

|  |  |  |  |
| --- | --- | --- | --- |
|  | fP​(p,α,β,a=0,c)=α​βcα​pα−1​(1−(p/c)α)β−1,f_{P}(p;\alpha,\beta,a=0,c)=\frac{\alpha\beta}{c^{\alpha}}\,p^{\alpha-1}\,(1-(p/c)^{\alpha})^{\beta-1}, |  | (52) |

over the support (0,c)(0,c). The rescaled Kumaraswamy-Binomial distribution then has PMF:

|  |  |  |  |
| --- | --- | --- | --- |
|  | P⁡(X=x,α,β,c,n)=(nx)​α​βcα​∫0cpx+α−1​(1−p)n−x​(1−(pc)α)β−1​𝑑p.P(X=x;\alpha,\beta,c,n)=\binom{n}{x}\;\frac{\alpha\,\beta}{c^{\alpha}}\int_{0}^{c}p^{\,x+\alpha-1}\,(1-p)^{n-x}\,\Bigl(1-\bigl(\tfrac{p}{c}\bigr)^{\alpha}\Bigr)^{\beta-1}\,dp. |  | (53) |

One can perform a change of variable p​=defczp\defeq cz, but simplifying yields sums of hypergeometric functions that add little conceptual clarity and so we resort to numerical integration using Python’s [mpmath library](https://mpmath.org/) ([mpmath development team, 2023](#bib.bib74)).

## Appendix H Maximum Likelihood Estimation of Scaled Beta-Negative Binomial Distribution

To model the distribution of passi​@​1\operatorname{pass_{i}@1}, we can perform maximum likelihood estimation on a scaled three-parameter Beta-Negative Binomial distribution. Recall that the scaled three parameter Beta distribution is:

|  |  |  |  |
| --- | --- | --- | --- |
|  | fP​(p,α,β,a=0,c)=pα−1​(c−p)β−1cα+β−1​B⁡(α,β).f_{P}(p;\alpha,\beta,a=0,c)=\frac{p^{\alpha-1}(c-p)^{\beta-1}}{c^{\alpha+\beta-1}\operatorname{B}(\alpha,\beta)}. |  | (54) |

We want the PMF of a three-parameter Beta-Negative Binomial distribution based on this scaled Beta distribution. For rr desired successes, the PMF that we first draw xx failures is:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | P⁡(X=x,α,β,c,r)\displaystyle P(X=x;\alpha,\beta,c,r) | =∫0c(x+r−1x)​pr​(1−p)x⏟NegBin​(r,p)​pα−1​(c−p)β−1cα+β−1​B​(α,β)⏟scaled Beta PDF​𝑑p\displaystyle=\;\int_{0}^{c}\underbrace{\binom{x+r-1}{x}\,p^{r}\,(1-p)^{x}}_{\text{NegBin}(r,p)}\;\;\underbrace{\frac{p^{\alpha-1}\,(c-p)^{\beta-1}}{\,c^{\alpha+\beta-1}\,\mathrm{B}(\alpha,\beta)\,}}_{\text{scaled Beta PDF}}\;dp |  | (55) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =(x+r−1x)​1cα+β−1​B​(α,β)​∫0cpr+α−1​(1−p)x​(c−p)β−1​𝑑p.\displaystyle=\;\binom{x+r-1}{x}\;\frac{1}{c^{\alpha+\beta-1}\,\mathrm{B}(\alpha,\beta)}\int_{0}^{c}p^{\,r+\alpha-1}\,\bigl(1-p\bigr)^{x}\,\bigl(c-p\bigr)^{\beta-1}\;dp. |  | (56) |

Next, substitute p=c​z⟹d​p=c​d​zp\;=\;c\,z\Longrightarrow dp\;=\;c\,dz
which rescales the domain [0,c][0,c] to [0,1][0,1]. Under this change:

|  |  |  |
| --- | --- | --- |
|  | pr+α−1=(c​z)r+α−1=cr+α−1​zr+α−1,p^{\,r+\alpha-1}\;=\;(c\,z)^{\,r+\alpha-1}\;=\;c^{\,r+\alpha-1}\;z^{\,r+\alpha-1}, |  |

|  |  |  |
| --- | --- | --- |
|  | (c−p)β−1=(c−c​z)β−1=(c⁡(1−z))β−1=cβ−1​(1−z)β−1,(c-p)^{\beta-1}\;=\;\bigl(c-c\,z\bigr)^{\beta-1}\;=\;\bigl(c(1-z)\bigr)^{\beta-1}\;=\;c^{\,\beta-1}\,(1-z)^{\beta-1}, |  |

|  |  |  |
| --- | --- | --- |
|  | (1−p)x=(1−c​z)x.(1-p)^{x}\;=\;\bigl(1-c\,z\bigr)^{x}. |  |

Putting these into the integrand:

|  |  |  |
| --- | --- | --- |
|  | pr+α−1​(1−p)x​(c−p)β−1​d​p=(cr+α−1​zr+α−1)​((1−c​z)x)​(cβ−1​(1−z)β−1)​(c​d​z).\displaystyle p^{\,r+\alpha-1}\,\bigl(1-p\bigr)^{x}\,\bigl(c-p\bigr)^{\beta-1}\,dp=\;\Bigl(c^{\,r+\alpha-1}\,z^{\,r+\alpha-1}\Bigr)\;\Bigl(\bigl(1-cz\bigr)^{x}\Bigr)\;\Bigl(c^{\,\beta-1}\,(1-z)^{\beta-1}\Bigr)\;\bigl(c\,dz\bigr). |  |

Factor out the constants in cc:

|  |  |  |
| --- | --- | --- |
|  | =cr+α−1​cβ−1​c​zr+α−1​(1−c​z)x​(1−z)β−1​d​z.=\;c^{\,r+\alpha-1}\;c^{\,\beta-1}\;c\;\;z^{\,r+\alpha-1}\,(1-cz)^{x}\,(1-z)^{\beta-1}\;dz. |  |

Since cr+α−1⋅cβ−1⋅c=cr+α+β−1c^{\,r+\alpha-1}\cdot c^{\,\beta-1}\cdot c\;=\;c^{\,r+\alpha+\beta-1}, we get

|  |  |  |
| --- | --- | --- |
|  | pr+α−1​(1−p)x​(c−p)β−1​d​p=cr+α+β−1​zr+α−1​(1−z)β−1​(1−c​z)x​d​z.p^{\,r+\alpha-1}\,(1-p)^{x}\,(c-p)^{\beta-1}\,dp\;=\;c^{\,r+\alpha+\beta-1}\,\,z^{\,r+\alpha-1}\,(1-z)^{\beta-1}\,(1-cz)^{x}\;\,dz. |  |

Plugging back into P⁡(X=x,α,β,c,r)P(X=x;\alpha,\beta,c,r) and simplifying:

|  |  |  |  |
| --- | --- | --- | --- |
|  | P⁡(X=x,α,β,c,r)=(x+r−1x)​crB⁡(α,β)​∫01zr+α−1​(1−z)β−1​(1−c​z)x​𝑑z.P(X=x;\alpha,\beta,c,r)=\;\binom{x+r-1}{x}\;\frac{c^{r}}{\mathrm{B}(\alpha,\beta)}\;\;\int_{0}^{1}z^{\,r+\alpha-1}\,(1-z)^{\beta-1}\,\bigl(1-c\,z\bigr)^{x}\,dz. |  | (57) |

We can re-express this using the [(Gauss) hypergeometric function](https://en.wikipedia.org/wiki/Hypergeometric_function#Euler_type) 2F1(⋅,⋅;⋅;⋅)\mathchoice{\mathop{}\kern 4.48613pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}{\mathop{}\kern 4.48613pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}{\mathop{}\kern 3.90283pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}{\mathop{}\kern 3.90283pt\mathopen{\vphantom{F}}_{\mathmakebox[0pt][r]{2}}}F_{1}(\cdot,\cdot;\cdot;\cdot):

|  |  |  |  |
| --- | --- | --- | --- |
|  | P⁡(X=x,α,β,c,r)=(x+r−1x)​cr​B​(r+α,β)B⁡(α,β)​F12​(−x,r+α,r+α+β,c).P(X=x;\alpha,\beta,c,r)\;=\;\binom{x+r-1}{x}\;\frac{c^{r}\,\mathrm{B}\bigl(r+\alpha,\;\beta\bigr)}{\mathrm{B}\bigl(\alpha,\;\beta\bigr)}\;\;{}_{2}F_{1}\!\Bigl(-x,\;r+\alpha;\;r+\alpha+\beta;\;c\Bigr). |  | (58) |
