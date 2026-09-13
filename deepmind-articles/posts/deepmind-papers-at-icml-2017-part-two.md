---
title: "DeepMind papers at ICML 2017 (part two)"
source: https://deepmind.google/blog/deepmind-papers-at-icml-2017-part-two/
site: deepmind
date: 2017-08-04
authors: 
crawled: 2026-09-13
---

The second of our three-part series, which gives an overview of the papers we are presenting at the ICML 2017 Conference in Sydney, Australia.

## Why is Posterior Sampling Better than Optimism for Reinforcement Learning?

**Authors:** Ian Osband, Benjamin Van Roy

Computational results demonstrate that posterior sampling for reinforcement learning (PSRL) dramatically outperforms existing algorithms driven by optimism, such as UCRL2. We provide insight into the extent of this performance boost and the phenomenon that drives it. We leverage this insight to establish an $\tilde{O}(H\sqrt{SAT})$ Bayesian regret bound for PSRL in finite-horizon episodic Markov decision processes. This improves upon the best previous Bayesian regret bound of $\tilde{O}(H S \sqrt{AT})$ for any reinforcement learning algorithm. Our theoretical results are supported by extensive empirical evaluation.

For further details and related work, please see the [paper](https://arxiv.org/abs/1607.00215).

**Check it out at ICML:**

Monday 07 August, 11:42-12:00 @ C4.5 (Talk)

Monday 07 August, 18:30-22:00 @ Gallery #36 (Poster)

## DARLA: Improving Zero-Shot Transfer in Reinforcement Learning

**Authors:** Irina Higgins\*, Arka Pal\*, Andrei Rusu, Loic Matthey, Chris Burgess, Alexander Pritzel, Matt Botvinick, Charles Blundell, Alexander Lerchner

Modern deep reinforcement learning agents rely on large quantities of data to learn how to act. In some scenarios, such as robotics, obtaining a lot of training data may be infeasible. Hence such agents are often trained on a related task where data is easy to obtain (e.g. simulation) with the hope that the learnt knowledge will generalise to the task of interest (e.g. reality). We propose DARLA, a DisentAngled Representation Learning Agent, that exploits its interpretable and structured vision to learn how to act in a way that is robust to various novel changes in its environment - including a simulation to reality transfer scenario in robotics. We show that DARLA significantly outperforms all baselines, and that its performance is crucially dependent on the quality of its vision.

For further details and related work, please see the [paper](http://arxiv.org/abs/1707.08475).

**Check it out at ICML:**

Monday 07 August, 16:42-17:00 @ C4.5 (Talk)\

Monday 07 August, 18:30-22:00 @ Gallery #123 (Poster)

## Automated Curriculum Learning for Neural Networks

**Authors:** Alex Graves, Marc G. Bellemare, Jacob Menick, Koray Kavukcuoglu, Remi Munos

As neural networks are applied to ever more complex problems, the need for efficient curriculum learning becomes more pressing. However, designing effective curricula is difficult and typically requires a large amount of hand-tuning. This paper uses reinforcement learning to automate the path, or syllabus, followed by the network through the curriculum so as to maximise the overall rate of learning progress. We consider nine different progress indicators, including a novel class of complexity-gain signal. Experimental results on three problems show that an automatically derived syllabus can lead to efficient curriculum learning, even on data (such as the bAbI tasks) that were not explicitly designed for curriculum learning.

For further details and related work, please see the [paper](https://arxiv.org/abs/1704.03003).

**Check it out at ICML:**

Monday 07 August, 16:42-17:00 @ C4.6 & C4.7 (Talk)

Monday 07 August, 18:30-20:00 @ Gallery #127 (Poster)

## Learning to learn without gradient descent by gradient descent

**Authors:** Yutian Chen, Matthew Hoffman, Sergio Gomez, Misha Denil, Timothy Lillicrap, Matthew Botvinick , Nando de Freitas

We learn recurrent neural network optimisers trained on simple synthetic functions by gradient descent. The learned optimisers exhibit a remarkable degree of transfer in that they can be used to efficiently optimise a broad range of derivative-free black-box problems, including continuous bandits, control problems, global optimization benchmarks and hyper-parameter tuning tasks.

For further details and related work, please see the [paper](https://arxiv.org/abs/1611.03824).

**Check it out at ICML:**

Monday 07 August, 17:15-17:33 @ Darling Harbour Theatre (Talk)

Tuesday 08 August, 18:30-22:00 @ Gallery #6 (Poster)

## A Distributional Perspective on Reinforcement Learning

**Authors:** Marc G. Bellemare\*, Will Dabney\*, Remi Munos

We argue for the fundamental importance of the value distribution: the distribution of the random return received by a reinforcement learning agent. This is in contrast to the common approach to reinforcement learning which models the expectation of this return, or value. Although there is an established body of literature studying the value distribution, thus far it has always been used for a specific purpose such as implementing risk-aware behaviour. We begin with theoretical results in both the policy evaluation and control settings, exposing a significant distributional instability in the latter. We then use the distributional perspective to design a new algorithm which applies Bellman's equation to the learning of approximate value distributions. We evaluate our algorithm using the suite of games from the Arcade Learning Environment. We obtain both state-of-the-art results and anecdotal evidence demonstrating the importance of the value distribution in approximate reinforcement learning. Finally, we combine theoretical and empirical evidence to highlight the ways in which the value distribution impacts learning in the approximate setting.

For further details and related work, please see the [blog post](https://deepmind.com/blog/article/going-beyond-average-reinforcement-learning) and the [paper](https://arxiv.org/abs/1707.06887).

**Check it out at ICML:**

Monday 07 August, 17:33-17:51 @ C4.5 (Talk)

Tuesday 08 August, 18:30-22:00 @ Gallery #13 (Poster)

## A Laplacian Framework for Option Discovery in Reinforcement Learning

**Authors:** Marlos Machado (Univ. Alberta), Marc G. Bellemare, Michael Bowling

Representation learning and option discovery are two of the biggest challenges in reinforcement learning (RL). Proto-value functions (PVFs) are a well-known approach for representation learning in MDPs. In this paper we address the option discovery problem by showing how PVFs implicitly define options. We do it by introducing eigenpurposes, intrinsic reward functions derived from learned representations. The options discovered from eigenpurposes traverse the principal directions of the state space. They are useful for multiple tasks because they are discovered without taking the environment’s rewards into consideration. Moreover, different options act at different time scales, making them helpful for exploration. We demonstrate features of eigenpurposes in traditional tabular domains as well as in Atari 2600 games.

For further details and related work, please see the [paper](http://proceedings.mlr.press/v70/machado17a/machado17a.pdf).

**Check it out at ICML:**

Monday 07 August, 18:09-18:27 @ C4.5 (Talk)

Tuesday 08 August 18:30-20:00 @ Gallery #23 (Poster)

## Neural Audio Synthesis of Musical Notes with WaveNet Autoencoders

**Authors:** Sander Dieleman, Karen Simonyan, Jesse Engel (Google Brain), Cinjon Resnick (Google Brain), Adam Roberts (Google Brain), Douglas Eck (Google Brain), Mohammad Norouzi (Google Brain)

In this paper, we introduce a powerful new WaveNet-style autoencoder model that conditions an autoregressive decoder on temporal codes learned from the raw audio waveform. We also introduce NSynth, a large-scale and high-quality dataset of musical notes that is an order of magnitude larger than comparable public datasets. Using NSynth, we demonstrate improved qualitative and quantitative performance of the WaveNet autoencoder over a well-tuned spectral autoencoder baseline. Finally, we show that the model learns a manifold of embeddings that allows for morphing between instruments, meaningfully interpolating in timbre to create new types of sounds that are realistic and expressive.

For further details and related work, please see the [paper](https://arxiv.org/abs/1704.01279).

**Check it out at ICML:**

Tuesday 08 August, 14:42-15:00 @ Parkside 1 (Talk)

Tuesday 08 August, 18:30-22:00 @ Gallery #98 (Poster)
