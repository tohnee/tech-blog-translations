---
title: "How is RLHF different from DPO at a high level?"
source: https://sebastianraschka.com/faq/docs/rlhf-vs-dpo.html
crawled: 2026-09-06
---

# How is RLHF different from DPO at a high level?

Classic **reinforcement learning from human feedback (RLHF)** trains a separate reward model from preference data and then uses that model to score responses generated during policy optimization. **Direct Preference Optimization (DPO)** removes the explicit reward-model and reinforcement-learning stages. It updates the language model directly from chosen and rejected responses.

Both methods usually begin with a model that has already received supervised instruction finetuning. They can also use the same kind of human preference record:

- a prompt (x)
- a chosen response (y\_w)
- a rejected response (y\_l)

The difference is how that comparison becomes a policy update.

| Property | Classic RLHF | DPO |
| --- | --- | --- |
| Preference data | Rankings or chosen-rejected responses | Chosen-rejected responses |
| Separate reward model | Yes | No |
| Policy training data | Responses sampled as the policy is optimized | Usually a fixed offline preference dataset |
| Update | Reinforcement-learning objective, often PPO | Pairwise classification-style loss |
| Reference policy | Usually used through a KL penalty | Used directly in the preference loss |
| Main systems challenge | Coordinating rollout, reward, reference, and policy components | Computing and tuning policy-reference likelihood ratios |

In the classic RLHF pipeline popularized for LLM post-training by the [InstructGPT paper](https://arxiv.org/abs/2203.02155), supervised finetuning first produces an initial policy. That policy generates several responses for selected prompts, and people rank or compare them. A **reward model** learns to assign a larger scalar score to the preferred response.

The policy then generates new responses during reinforcement-learning updates. An algorithm such as Proximal Policy Optimization (PPO) increases expected reward. A KL penalty discourages the policy from moving too far from a frozen reference model, which is commonly the supervised-finetuned checkpoint.

![The classic RLHF pipeline uses supervised finetuning, preference collection, a learned reward model, and reinforcement-learning updates such as PPO.](https://sebastianraschka.com/images/LLMs-from-scratch-images/dpo/4.webp)

This setup is powerful because the reward model can score responses that were not part of the original comparison dataset. The current policy can keep sampling new outputs as it changes. That online component also creates difficulty. Training has to coordinate generation, reward scoring, policy updates, KL control, and often a value model. The learned reward is only a proxy for the desired behavior, so aggressive optimization can exploit weaknesses in the reward model.

DPO starts from the same KL-regularized preference-learning view. It rewrites the optimization problem into a loss over response pairs. For policy (\pi\_\theta), frozen reference policy (\pi\_{\text{ref}}), and scale (\beta), the standard DPO loss is

[
\mathcal{L}*{\text{DPO}}
= -\log \sigma \left(
\beta
\left[
\log \frac{\pi*\theta(y\_w \mid x)}
{\pi\_{\text{ref}}(y\_w \mid x)}
-
\log \frac{\pi\_\theta(y\_l \mid x)}
{\pi\_{\text{ref}}(y\_l \mid x)}
\right]
\right).
]

The response probabilities are sequence probabilities, usually represented as sums of token log probabilities. Training increases the policy’s relative odds of the chosen response compared with the rejected response, measured against the same odds under the reference policy. This is more specific than increasing the chosen response likelihood alone.

The parameter (\beta) sets the scale of this preference logit and comes from the KL-regularized derivation. It needs to be tuned together with the learning rate, data, and number of training steps. The frozen reference policy anchors the update. Some later preference methods remove or alter this reference term, but standard DPO includes it.

![DPO applies one direct objective to the chosen-rejected response pair and avoids a separately trained reward model plus PPO loop.](https://sebastianraschka.com/images/LLMs-from-scratch-images/dpo/5.webp)

Standard DPO is an **offline** method. The preference pairs are fixed before training, so the policy does not have to generate fresh responses inside every optimization iteration. Training resembles ordinary supervised learning and is usually easier to implement and reproduce than a full PPO-based RLHF stack.

DPO still has meaningful computation and memory costs. It needs log probabilities for both responses under the trainable policy and the reference policy. Reference log probabilities can be precomputed for a fixed dataset, although the policy still evaluates chosen and rejected sequences. Memory use, sequence length, padding masks, and response-token masking remain practical concerns.

The offline dataset also limits what DPO observes directly. As the policy changes, it may produce outputs unlike either response in the stored pairs. Classic online RLHF can sample from the changing policy and evaluate those new outputs with the reward model. Whether that flexibility helps depends on reward-model quality and the stability of the RL procedure.

Both methods inherit the limitations of their preference data. Annotators may favor longer answers, familiar writing styles, excessive agreement, or other superficial properties. A chosen response may still be wrong if it was merely better than a weak alternative. DPO can overfit these pairwise signals, while RLHF can overoptimize the learned reward.

The term **RLHF** is also used loosely. Some discussions use it for any post-training method based on human preferences, including DPO. On this page, RLHF refers to the classic reward-model-plus-RL pipeline, and DPO refers to the offline direct objective introduced in the [DPO paper](https://arxiv.org/abs/2305.18290).

For a small or transparent training stack, I would usually start with supervised finetuning and DPO. The fixed pair dataset makes failures easier to reproduce and inspect. A classic RLHF pipeline becomes more attractive when fresh policy exploration, a reusable scalar reward model, or several reward sources justify the additional machinery.

Method choice does not replace evaluation. Compare the final checkpoints on held-out preference pairs, task correctness, formatting, safety criteria, response length, and capabilities that should be retained from the starting model. The related FAQ [What is DPO, and how does it differ from supervised finetuning?](https://sebastianraschka.com/faq/docs/dpo-vs-supervised-finetuning.html) explains the preceding SFT-to-DPO transition.
