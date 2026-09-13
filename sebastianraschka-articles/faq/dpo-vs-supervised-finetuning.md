---
title: "Direct Preference Optimization vs. Supervised Finetuning"
source: https://sebastianraschka.com/faq/docs/dpo-vs-supervised-finetuning.html
crawled: 2026-09-06
---

# Direct Preference Optimization vs. Supervised Finetuning

**Supervised finetuning (SFT)** and **Direct Preference Optimization (DPO)** differ in the training examples they consume and in the probability relationships optimized by their loss functions.

Both methods use labeled data and gradient descent. In this comparison, *supervised finetuning* is the conventional name for demonstration-based SFT rather than a claim that DPO is unsupervised.

For SFT, one record contains a prompt and a target response. Training increases the token-level likelihood of that response. If the prompt asks for a short explanation of gradient descent, for example, the target shows the model the particular answer it should learn to reproduce.

DPO uses two responses to the same prompt. One is marked **chosen** and the other **rejected**. The labels express a preference between the pair. They do not require the chosen response to be the only valid answer.

During DPO training, the model compares the sequence log probabilities of the chosen and rejected responses. It learns to increase the gap in favor of the chosen response. A frozen reference model, usually a copy of the model before DPO begins, provides an anchor so that the updated policy does not drift freely away from its starting behavior.

![DPO starts from the idea that multiple responses may be valid but some are preferred over others](https://sebastianraschka.com/images/LLMs-from-scratch-images/dpo/2.webp)

This setup is useful when several responses are plausible and the distinction concerns quality. One answer may follow the requested format more closely, explain a step more clearly, or avoid an unsupported claim. SFT can learn from a polished demonstration. DPO additionally learns which features made one response preferable to another in the supplied pair.

The common training order is base-model pretraining, followed by SFT and then DPO. SFT first gives the model a reasonable instruction-following policy. DPO then adjusts relative preferences among responses that the model is already capable of producing. This order is common practice rather than a strict requirement of the DPO loss.

Compared with a classic RLHF pipeline, DPO removes two major pieces of machinery. It does not fit a separate reward model and then optimize the language model with a reinforcement-learning algorithm. The preference objective is applied directly to the language model using ordinary gradient-based training.

![The repo's DPO overview emphasizes direct optimization from preference pairs instead of a full RLHF pipeline](https://sebastianraschka.com/images/LLMs-from-scratch-images/dpo/5.webp)

Preference labels need careful interpretation. A chosen answer can still contain problems if it was merely the better of two weak candidates. Repeated preferences for verbosity, certain phrases, or a narrow response format can also be learned more strongly than intended. Pair construction and review are therefore as important as the optimization method.

The chapter 7 DPO notebook in the repo uses a small learning rate and a modest training duration. Those conservative settings are sensible because overly aggressive preference optimization can degrade general response quality. In practice, I would use SFT to establish the desired task behavior and add DPO when chosen-versus-rejected comparisons provide information that a single target response does not capture as directly.
