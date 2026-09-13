---
title: "How confessions can keep language models honest"
date: 2025-12-03
source: https://openai.com/index/how-confessions-can-keep-language-models-honest/
crawled: 2026-09-13
category: research
---

AI systems are becoming more capable, and we want to understand them as deeply as possible—including how and why they arrive at an answer. Sometimes a model takes a shortcut or optimizes for the wrong objective, but its final output still looks correct. If we can surface when that happens, we can better monitor deployed systems, improve training, and increase trust in the outputs.

Research by OpenAI and others has shown that AI models can [hallucinate](https://openai.com/index/introducing-simpleqa/), reward-hack, or be dishonest. At the moment, we see the most concerning misbehaviors, such as [scheming](https://www.antischeming.ai/), only in stress-tests and adversarial evaluations. But as models become more capable and increasingly agentic, even rare forms of misalignment become more consequential, motivating us to invest in methods that help us better detect, understand, and mitigate these risks.

This work explores one such approach: training models to explicitly admit when they engage in undesirable behavior—a technique we call **confessions**.

A confession is a second output, separate from the model’s main answer to the user. The main answer is judged across many dimensions—correctness, style, helpfulness, compliance, safety, and more, and these multifaceted signals are used to train models to produce better answers. The confession, by contrast, is judged and trained on one thing only: honesty. Borrowing a page from the structure of a confessional, nothing the model says in its confession is held against it during training. If the model honestly admits to hacking a test, sandbagging, or violating instructions, that admission increases its reward rather than decreasing it. The goal is to encourage the model to faithfully report what it actually did.

In our tests, we found that the confessions method significantly improves the visibility of model misbehavior. Averaging across our evaluations designed to induce misbehaviors, the probability of “false negatives” (i.e., the model not complying with instructions and then not confessing to it) is only 4.4%.

#### Confession accuracy

Accuracy of our “proof of concept” confession model on a number of adversarial datasets. Outcomes are categorized as complied and didn’t confess (true negative), complied and confessed (false positive), didn’t comply and didn’t confess (false negative), and didn’t comply and confessed (true positive).

Given a user prompt, the four possible outcomes are based on the combination of (1) whether the model response is compliant (“good”) or non-compliant (“bad”), and (2) whether the confession is claims compliance or non-compliance. We generally see that confessions are very likely to be accurate, and furthermore confession errors are typically benign, and due to honest confusion rather than intentionally misleading.

## How confessions work

A confession is a self-report by the model of how well it complied with both the spirit and the letter of explicit and implicit instructions or policies that it was given, and whether there were any instances in which it “cut corners” or “hacked”, violated policies, or in any way fell short of expectations. In our research, we find that models can be trained to be candid in reporting their own shortcomings. We trained a version of GPT‑5 Thinking to produce confessions, and evaluated it on a number of out-of-distribution stress-test datasets designed to elicit behaviors such as scheming, hacking, violating instructions, and hallucinations. We found that even when the model engages in these undesirable behaviors, it is very likely to confess to them. The figure above shows that the confession approach is broadly effective across a diverse array of datasets and tasks.

Following any interaction between the user and the model ending in a model answer, a confession can be requested by sending the model a “system message” that instructs the model to provide a confession report. The report pertains to the last answer by the model, and includes (1) the list of all explicit and implicit instructions, constraints, and objectives that this answer should have satisfied, (2) an honest and objective analysis whether the answer did in fact satisfy each one of these objectives, and (3) a list of any uncertainties, ambiguities, or “tough judgement calls” that the model encountered in producing the answer. During training, a confession is evaluated by a separate reward model that scores only the confession on completeness of objectives, accuracy of the compliance analysis, and coverage of uncertainties. These rewards are applied exclusively to the confession output and never influence the reward for the main answer. This ensures the property, discussed above, that nothing the model says in confession can hurt (or help) its reward for its main answer.

## Why confessions work

The theory behind confessions is simple. Many kinds of unwanted model behavior appear because we ask the model to optimize for several goals at once. During reinforcement learning, the model sees a prompt, produces a response, and gets a reward. Over time, it learns to produce the kinds of answers that score well. The challenge is that the reward signal has to combine many different considerations at once: how correct the answer is, whether it’s helpful, whether it follows product and policy specifications, whether it meets safety constraints, and whether it matches what users tend to prefer. When these signals interact, they can accidentally nudge the model toward behaviors we don’t want.

For example, our work on [hallucinations](https://openai.com/index/why-language-models-hallucinate/) showed that some datasets reward a confident guess more than an honest admission of uncertainty. Our research on [sycophancy](https://openai.com/index/expanding-on-sycophancy/) showed that models can become overly agreeable when the preference signal is too strong. And [work](https://arxiv.org/abs/2406.10162) from other groups have shown that models can “reward hack”—finding loopholes in the training setup that let them earn a high score without truly doing what we intended. In some cases, these shortcuts can [generalize](https://www.anthropic.com/research/emergent-misalignment-reward-hacking) to even more pernicious behavior in deployment.

Confessions avoid this issue by separating the objectives entirely. The main answer continues to optimize for all the usual factors. The confession is trained on exactly one: honesty. Nothing the model says in the confession is held against it, and the confession does not influence the reward for the main answer. That means even if the model deceives or cuts corners in its original output, it still has an incentive to admit that in the confession. This is what we see in practice: models are willing to acknowledge bad behavior in the confession, even in cases where they hide it in the main answer. And when confessions fail, it is usually because the model is genuinely confused—because the instructions were ambiguous or because it didn’t realize a mistake had been made—rather than because it was deliberately trying to mislead. Importantly, the early results show that confessions remain effective even when the original answer is produced with no chain-of-thought at all, suggesting that confession honesty does not depend on internal reasoning legibility and may generalize across future model architectures.

Confession training works even without ground-truth labels of compliance. By “ground truth,” we mean a definitive, externally provided label indicating whether the model actually followed an instruction or violated it. In many real-world tasks these labels are unavailable—if we knew with certainty that the model had violated a rule, we could directly penalize that violation rather than relying on a confession. Instead, the model is rewarded for producing a structured, evidence-backed explanation of what it believes it did. The paper shows that honesty tends to emerge under this setup. We think this is because providing a truthful, evidence-supported account is generally easier for the model than constructing a coherent fabricated narrative that can pass the judge. This is a key assumption explored in the paper, which also discusses the cases in which confessions fail—the false negatives and false positives—and how they arise.

The paper provides initial evidence that confessions work, but should not be construed as a definitive proof. While we used a frontier model (GPT‑5 Thinking), our experiments were limited in scale, using a relatively small amount of computation and data. We are excited about taking this work to the next level, and seeing if confessions’ honesty will continue to hold as we scale up its training.

## Examples of confessions

## What we learned

As part of our experiments we deliberately trained models against a “hackable” reward signal computed by a weaker model. This setup applied to both the main reward and the confession reward. The model learned to exploit the weak reward signal: its apparent accuracy (when judged by the weak model) improved, while its true accuracy (when judged by a stronger evaluator) fell.

However, even though the confession channel was trained on the same weak signal, its accuracy moved in the opposite direction. The model learned that the best way to optimize confession reward was simply to admit when it hacked the main reward. Confessions became more accurate over time, even as the main behavior drifted.

Over the course of training, when the model fails to comply, it learns in some fraction of the cases to “hack” the main reward judge and so the judge accuracy is decreasing. In contrast, even though the confession reward judge is just as hackable, the model only becomes more honest over training in its confession, eventually reaching near 100% of confessing when it did not comply.

The [paper](https://arxiv.org/abs/2512.08093) contains more experiments and results. We compared the confession-trained model against a control model trained in the same way but without the confession channel. We also examined the cases where confessions failed. Almost all of the “misses” occurred when the model was genuinely confused—when the instructions were ambiguous or when it simply didn’t realize it had made a mistake. (See the false negative example above.)

## Limitations

Confessions have their limitations. They do not prevent bad behavior; they surface it. Their main value is as a monitoring and diagnostic tool, both during training and in deployment. Confessions play a similar role to [chain-of-thought monitoring](https://openai.com/index/chain-of-thought-monitoring/): both make hidden reasoning processes more visible. Confessions focus on whether the model violated instructions; chain-of-thought can highlight how it arrived there.

This work is also a proof of concept. We did not train confession mechanisms at large scale, and confession accuracy is still imperfect. There is more work to be done to make the approach more reliable, more robust, and more broadly applicable across model families and tasks.

## Looking ahead

This work fits within our [broader approach to AI safety](https://openai.com/safety/how-we-think-about-safety-alignment/). Confessions are one mechanism in a larger stack that includes [deliberative alignment](https://openai.com/index/deliberative-alignment/), [chain-of-thought monitoring](https://openai.com/index/chain-of-thought-monitoring/), [instruction hierarchy](https://openai.com/index/the-instruction-hierarchy/), and more. No single method is enough; the goal is a layered system of checks and transparency tools that reinforce each other. Confessions can help with diagnosing problematic behaviors in models during training and evaluation, as well as monitoring during deployment. Confessions by themselves do not solve the problem of balancing multiple dimensions. But by creating a “truth serum” mode in which models are solely focused on honesty, it adds a valuable tool to our stack for improving honesty and safety across the board.

As models become more capable and are deployed in higher-stakes settings, we need better tools for understanding what they are doing and why. Confessions are not a complete solution, but they add a meaningful layer to our transparency and oversight stack. In future work, we plan to scale up confessions, as well as pair them with complementary transparency and safety techniques, including chain-of-thought monitoring and deliberative alignment, to make further progress toward ensuring that our models faithfully obey all instructions and policies (such as our [Model Spec](https://model-spec.openai.com/)), and truthfully report on their actions.
