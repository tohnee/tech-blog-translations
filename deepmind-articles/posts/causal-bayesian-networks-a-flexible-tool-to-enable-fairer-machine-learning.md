---
title: "Causal Bayesian Networks: A flexible tool to enable fairer machine learning"
source: https://deepmind.google/blog/causal-bayesian-networks-a-flexible-tool-to-enable-fairer-machine-learning/
site: deepmind
date: 2019-10-03
authors: Silvia Chiappa, William Isaac
crawled: 2026-09-13
---

Decisions based on machine learning (ML) are potentially advantageous over human decisions, as they do not suffer from the same subjectivity, and can be more accurate and easier to analyse. At the same time, data used to train ML systems often contain human and societal biases that can lead to harmful decisions: extensive evidence in areas such as hiring, criminal justice, surveillance, and healthcare suggests that ML decision systems can treat individuals unfavorably (unfairly) on the basis of characteristics such as race, gender, disabilities, and sexual orientation – referred to as sensitive attributes.

Currently, most fairness criteria used for evaluating and designing ML decision systems focus on the relationships between the sensitive attribute and the system output. However, the training data can display different patterns of unfairness depending on how and why the sensitive attribute influences other variables. Using such criteria without fully accounting for this could be problematic: it could, for example, lead to the erroneous conclusion that a model exhibiting harmful biases is fair and, vice-versa, that a model exhibiting harmless biases is unfair. The development of technical solutions to fairness also requires considering the different, potentially intricate, ways in which unfairness can appear in the data.

Understanding how and why a sensitive attribute influences other variables in a dataset can be a challenging task, requiring both a technical and sociological analysis. The visual, yet mathematically precise, framework of [Causal](https://www.cambridge.org/gb/academic/subjects/philosophy/philosophy-science/causality?format=HB) [Bayesian](https://pdfs.semanticscholar.org/c4bc/ad0bb58091ecf9204ddb5db7dce749b0d461.pdf) [networks](https://mitpress.mit.edu/books/causation-prediction-and-search-second-edition) (CBNs) represents a flexible useful tool in this respect as it can be used to formalize, measure, and deal with different unfairness scenarios underlying a dataset. A CBN (Figure 1) is a graph formed by nodes representing random variables, connected by links denoting causal influence. By defining unfairness as the presence of a harmful influence from the sensitive attribute in the graph, CBNs provide us with a simple and intuitive **visual tool** for describing different possible unfairness scenarios underlying a dataset. In addition, CBNs provide us with a powerful **quantitative tool** to measure unfairness in a dataset and to help researchers develop techniques for addressing it.


### Characterising patterns of unfairness underlying a dataset

Consider a hypothetical college admission example ([inspired by the Berkeley case](https://science.sciencemag.org/content/187/4175/398)) in which applicants are admitted based on qualifications Q, choice of department D, and gender G; and in which female applicants apply more often to certain departments (for simplicity’s sake, we consider gender as binary, but this is not a necessary restriction imposed by the framework).

![A directed graph diagram featuring four colored circular nodes labeled G, Q, D, and A. Node G is light orange (top-left), Node Q is light pink (top-right), Node D is light purple (bottom-left), and Node A is light green (bottom-right). Blue arrows indicate directed relationships: a straight arrow points from G down to D, a diagonal arrow points from G to A, a horizontal arrow points from D to A, and a straight vertical arrow points from Q down to A. Each of the three arrows pointing directly into node A (from G, D, and Q) features a small dark blue perpendicular bar segment along its shaft.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227373238ec8fbd75178b8d_Visual20Tool.gif)

Figure 1. CBN representing a hypothetical college admission process.

**Definition: In a CBN, a path from node X to node Z is defined as a sequence of linked nodes starting at X and ending at Z. X is a cause of (has an influence on) Z if there exists a causal path from X to Z, namely a path whose links are pointing from the preceding nodes toward the following nodes in the sequence. For example, in Figure 1, the path G→D→A is causal, whilst the path G→D→A←Q is non causal.**

The admission process is represented by the CBN in Figure 1. Gender has a direct influence on admission through the causal path G→A and an indirect influence through the causal path G→D→A. The direct influence captures the fact that individuals with the same qualifications who are applying to the same department might be treated differently based on their gender. The indirect influence captures differing admission rates between female and male applicants due to their differing department choices.

Whilst the direct influence of the sensitive attribute on admission is considered unfair for social and legal reasons, the indirect influence could be considered fair or unfair depending on contextual factors. In Figure 2a, 2b and 2c, we depict three possible scenarios, where total or partial red paths are used to indicate unfair and and partially-unfair links, respectively.

![ A directed graph diagram featuring four colored circular nodes labeled G, Q, D, and A, with updated arrow patterns. Node G is light orange (top-left), Node Q is light pink (top-right), Node D is light purple (bottom-left), and Node A is light green (bottom-right). The diagonal arrow pointing from G to A is colored red with a small red bar segment along its shaft. The remaining arrows are blue: a straight vertical arrow from G to D containing a small blue bar segment, a clean horizontal arrow from D to A with no bar segment, and a straight vertical arrow from Q to A featuring a small blue bar segment.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227377c6ee3f3e2d131cc80_Fig202a.gif)

Figure 2a: In the first scenario, female applicants voluntarily apply to departments with low acceptance rates, and therefore the path G→D is considered fair.

![A directed graph diagram featuring four colored circular nodes labeled G, Q, D, and A, with a third set of arrow patterns. Node G is light orange (top-left), Node Q is light pink (top-right), Node D is light purple (bottom-left), and Node A is light green (bottom-right). The straight downward arrow from G to D is solid red with no bar segment, and the diagonal arrow from G to A is red with a red bar segment. The horizontal arrow from D to A is blue with a red bar segment along its shaft, and the straight vertical arrow from Q to A is blue with a blue bar segment.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227378d615f432d6239d29e_Fig202b.gif)

Figure 2b: In the second scenario, female applicants apply to departments with low acceptance rates due to systemic historical or cultural pressures, and therefore the path G→D is considered unfair (as a consequence, the path D→A becomes partially unfair).

![A directed graph diagram featuring four colored circular nodes labeled G, Q, D, and A. Node G is light orange (top-left), Node Q is light pink (top-right), Node D is light purple (bottom-left), and Node A is light green (bottom-right). The straight downward arrow from G to D is blue with a blue bar segment near the top, and the diagonal arrow from G to A is red with a red bar segment. The horizontal arrow from D to A is dual-colored, with a red shaft transitioning to a blue shaft, terminating in nested red and blue arrowheads with no bar segment. The straight vertical arrow from Q to A is blue with a blue bar segment.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622737ad2b83632313e16caf_Fig202c.gif)

Figure 2c: In the third scenario, the college lowers the admission rates for departments voluntarily chosen more often by women. The path G→D is considered fair, but the path D→A is partially unfair.

This simplified example shows how CBNs can provide us with a visual framework for describing different possible unfairness scenarios. Understanding which scenario underlies a dataset can be challenging or even impossible, and might require expert knowledge. It is nevertheless necessary to avoid pitfalls when evaluating or designing a decision system.

As an example, let’s assume that a university uses historical data to train a decision system to decide whether a prospective applicant should be admitted, and that a regulator wants to evaluate its fairness. Two popular fairness criteria are **statistical parity** (requiring the same **admission rates** among female and male applicants) and **equal false positive or negative rates** (EFPRs/EFNRs, requiring the same **error rates** among female and male applicants: i.e., the percentage of accepted applicants erroneously predicted as rejected, and vice-versa). In other words, statistical parity and EFPRs/EFNRs require all the predictions and the incorrect predictions to be independent of gender.

From the discussion above, we can deduce that whether such criteria are appropriate or not strictly depends on the nature of the data pathways. Due to the presence of the unfair direct influence of gender on admission, it would be inappropriate for the regulator to use EFPRs/EFNRs to gauge fairness, because this criterion considers the influence that gender has on admission in the data as legitimate. This means that it would be possible for the system to be deemed fair, even if it carries the unfair influence: this would automatically be the case for an error-free decision system. On the other hand, if the path G→D→A was considered fair, it would be inappropriate to use statistical parity. In this case, it would be possible for the system to be deemed unfair, even if it does not contain the unfair direct influence of gender on admission through the path G→A and only contains the fair indirect influence through the path G→D→A. In [our first paper](https://arxiv.org/abs/1907.06430), we raise these concerns in the context of the fairness debate surrounding the COMPAS pretrial risk assessment tool, which has been central to the dialogue around the risks of using ML decision systems.


### Path-specific (counterfactual) inference techniques for fairness

CBNs can also be used to quantify unfairness in a dataset and to design techniques for alleviating unfairness in the case of complex relationships in the data.

Path-specific techniques enable us to estimate the influence that a sensitive attribute has on other variables along specific sets of causal paths. This can be used to measure the degree of unfairness on a given dataset in complex scenarios in which some causal paths are considered unfair whilst other causal paths are considered fair. In the college admission example in which the path G→D→A is considered fair, path-specific techniques would enable us to measure the influence of G on A restricted to the direct path G→A over the whole **population**, in order to obtain an estimate of the degree of unfairness contained in the dataset.

**Sidenote: It's worth noting that, in our simple example, we do not consider the presence of confounders for the influence of G on A. In this case, as there are no unfair causal paths from G to A except the direct one, the degree of unfairness could simply be obtained by measuring the discrepancy between p(A | G=0, Q, D) and p(A | G=1, Q, D), where p(A | G=0, Q, D) indicates the distribution of A conditioned on the candidate being male, their qualifications, and department choice.**

The additional use of counterfactual inference techniques would enable us to ask if a specific **individual** was treated unfairly, for example by asking whether a rejected female applicant (G=1, Q=q, D=d, A=0) would have obtained the same decision in a counterfactual world in which her gender were male along the direct path G→A. In this simple example, assuming that the admission decision is obtained as the deterministic function f of G, Q, and D, i.e., A = f(G, Q, D), this corresponds to asking if f(G=0, Q=q, D=d) = 0, namely if a male applicant with the same department choice and qualifications would have also been rejected. We exemplify this in Figure 3 by re-computing the admission decision after changing the female candidate's photo to a male one in the profile.

![An illustration comparing a "Factual World" to a "Counterfactual World" to assess fairness. On the left (Factual World), a candidate profile shows a female avatar alongside variables "d" and "q". On the right (Counterfactual World), the same candidate profile maintains identical "d" and "q" variables, but the female avatar is replaced with a male avatar.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622737ecf51e736db2ea47f1_Fig203.gif)

Figure 3. Counterfactual scenario

However, path-specific counterfactual inference is generally more complex to achieve, if some variables are unfairly influenced by G. Assume that G also has an influence on Q through a direct path G→Q which is considered unfair. In this case, the CBN contains both variables that are fairly and unfairly influenced by G. Path-specific counterfactual inference would consist in performing a counterfactual correction of q, q\_0, i.e of the variable which is unfairly influenced by G, and then computing the counterfactual decision as f(G=0, Q=q\_0, D=d). The counterfactual correction q\_0 is obtained by first using the information of the female applicant (G=1, Q=q, D=d, A=0) and knowledge about the CBN to get an estimate of the specific latent randomness in the makeup of the applicant, and then using this estimate to re-compute the value of Q as if G=0 along G→Q.

In addition to answering questions of fairness in a dataset, path-specific counterfactual inference could be used to design methods to alleviate the unfairness of an ML system. In our [second paper](https://arxiv.org/abs/1802.08139), we propose a method to perform path-specific counterfactual inference and suggest that it can be used to post-process the unfair decisions of a trained ML system by replacing them with counterfactual decisions. The resulting system is said to satisfy path-specific counterfactual fairness.

## Conclusion

As machine learning continues to be embedded in more systems which have a significant impact on people’s lives and safety, it is incumbent on researchers and practitioners to identify and address potential biases embedded in how training data sets are generated. Causal Bayesian Networks offer a powerful visual and quantitative tool for expressing the relationships among random variables in a dataset. While it is important to acknowledge the limitations and difficulties of using this tool – such as identifying a CBN that accurately describes the dataset’s generation, dealing with confounding variables, and performing counterfactual inference in complex settings – this unique combination of capabilities could enable a deeper understanding of complex systems and allow us to better align decision systems with society's values.

**Notes**

This post is based on the following papers:

[A Causal Bayesian Networks Viewpoint on Fairness](https://arxiv.org/abs/1907.06430)

[Path-Specific Counterfactual Fairness](https://arxiv.org/abs/1802.08139)

With thanks to Niki Kilbertus, Ben Coppin, Tom Stepleton, Ray Jiang, Christina Heinze-Deml, Tom Everitt, and Shira Mitchell.
