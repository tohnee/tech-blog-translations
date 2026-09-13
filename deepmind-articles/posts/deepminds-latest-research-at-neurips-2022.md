---
title: "DeepMind’s latest research at NeurIPS 2022"
source: https://deepmind.google/blog/deepminds-latest-research-at-neurips-2022/
site: deepmind
date: 2022-11-25
authors: 
crawled: 2026-09-13
---

Advancing best-in-class large models, compute-optimal RL agents, and more transparent, ethical, and fair AI systems

The thirty-sixth International Conference on Neural Information Processing Systems ([NeurIPS 2022](https://nips.cc/Conferences/2022)) is taking place from 28 November - 9 December 2022, as a hybrid event, based in New Orleans, USA.

NeurIPS is the world’s largest conference in artificial intelligence (AI) and machine learning (ML), and we’re proud to support the event as Diamond sponsors, helping foster the exchange of research advances in the AI and ML community.

Teams from across DeepMind are presenting 47 papers, including 35 external collaborations in virtual panels and poster sessions. Here’s a brief introduction to some of the research we’re presenting:

## Best-in-class large models

Large models (LMs) – generative AI systems trained on huge amounts of data – have resulted in incredible performances in areas including language, text, audio, and image generation. Part of their success is down to their sheer scale.

However, in Chinchilla, we have created a [70 billion parameter language model that outperforms many larger models](https://www.deepmind.com/publications/an-empirical-analysis-of-compute-optimal-large-language-model-training), including Gopher. We updated the scaling laws of large models, showing how previously trained models were too large for the amount of training performed. This work already shaped other models that follow these updated rules, creating leaner, better models, and has won an [Outstanding Main Track Paper](https://blog.neurips.cc/2022/11/21/announcing-the-neurips-2022-awards/) award at the conference.

Building upon Chinchilla and our multimodal models NFNets and Perceiver, we also present [Flamingo, a family of few-shot learning visual language models](https://arxiv.org/abs/2204.14198). Handling images, videos and textual data, Flamingo represents a bridge between vision-only and language-only models. A single Flamingo model sets a new state of the art in few-shot learning on a wide range of open-ended multimodal tasks.

And yet, scale and architecture aren’t the only factors that are important for the power of transformer-based models. Data properties also play a significant role, which we discuss in a presentation on [data properties that promote in-context learning in transformer models](https://openreview.net/forum?id=lHj-q9BSRjF).

## Optimising reinforcement learning

Reinforcement learning (RL) has shown great promise as an approach to creating generalised AI systems that can address a wide range of complex tasks. It has led to breakthroughs in many domains from Go to mathematics, and we’re always looking for ways to make RL agents smarter and leaner.

We introduce a new approach that boosts the decision-making abilities of RL agents in a compute-efficient way by [drastically expanding the scale of information available for their retrieval](https://arxiv.org/abs/2206.05314).

We’ll also showcase a conceptually simple yet general approach for curiosity-driven exploration in visually complex environments – an RL agent called [BYOL-Explore](https://openreview.net/pdf?id=qHGCH75usg). It achieves superhuman performance while being robust to noise and being much simpler than prior work.

## Algorithmic advances

From compressing data to running simulations for predicting the weather, algorithms are a fundamental part of modern computing. And so, incremental improvements can have an enormous impact when working at scale, helping save energy, time, and money.

We share a radically new and highly scalable method for the [automatic configuration of computer networks](https://www.deepmind.com/publications/learning-to-configure-computer-networks-with-neural-algorithmic-reasoning), based on neural algorithmic reasoning, showing that our highly flexible approach is up to 490 times faster than the current state of the art, while satisfying the majority of the input constraints.

During the same session, we also present a rigorous exploration of the previously theoretical notion of “algorithmic alignment”, [highlighting the nuanced relationship between graph neural networks and dynamic programming](https://www.deepmind.com/publications/graph-neural-networks-are-dynamic-programmers), and how best to combine them for optimising out-of-distribution performance.

## Pioneering responsibly

At the heart of DeepMind’s mission is our commitment to act as responsible pioneers in the field of AI. We’re committed to developing AI systems that are transparent, ethical, and fair.

Explaining and understanding the behaviour of complex AI systems is an essential part of creating fair, transparent, and accurate systems. We offer a [set of desiderata that capture those ambitions, and describe a practical way to meet them](https://openreview.net/pdf?id=bk8vkdQfBS), which involves training an AI system to build a causal model of itself, enabling it to explain its own behaviour in a meaningful way.

To act safely and ethically in the world, AI agents must be able to reason about harm and avoid harmful actions. We’ll introduce collaborative work on a novel statistical measure called [counterfactual harm](https://arxiv.org/abs/2204.12993), and demonstrate how it overcomes problems with standard approaches to avoid pursuing harmful policies.

Finally, we're presenting our new paper which proposes [ways to diagnose and mitigate failures in model fairness caused by distribution shifts](https://www.deepmind.com/publications/diagnosing-failures-of-fairness-transfer-across-distribution-shift-in-real-world-medical-settings), showing how important these issues are for the deployment of safe ML technologies in healthcare settings.

See the full range of our work at NeurIPS 2022 [here](https://deepmind.events/events/neurips2022/resources).
