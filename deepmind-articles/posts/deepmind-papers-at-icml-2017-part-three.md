---
title: "DeepMind papers at ICML 2017 (part three)"
source: https://deepmind.google/blog/deepmind-papers-at-icml-2017-part-three/
site: deepmind
date: 2017-08-04
authors: 
crawled: 2026-09-13
---

The final part of our three-part series that gives an overview of the papers we are presenting at the ICML 2017 Conference in Sydney, Australia.

## Cognitive Psychology for Deep Neural Networks: A Shape Bias Case Study

**Authors:** Samuel Ritter\*, David Barrett\*, Adam Santoro, Matt Botvinick

Deep neural networks (DNNs) have achieved unprecedented performance on a wide range of tasks, rapidly outpacing our understanding of the nature of their solutions. In this work, we propose to address this interpretability problem in modern DNNs using the problem descriptions, theories and experimental methods developed of cognitive psychology. In a case study, we apply a theory and method from the psychology of human word learning to better understand how modern one-shot learning systems work. Results revealed not only that our DNNs exhibit the same inductive bias as humans, but also several unexpected features of the DNNs.

For further details and related work, please see the [paper](https://arxiv.org/pdf/1706.08606.pdf).

**Check it out at ICML:**

Tuesday 08 August, 15:48-16:06 @ Darling Harbour Theatre (Talk)

Tuesday 08 August, 18:30-20:00 @ Gallery #113 (Poster)

## Count-Based Exploration with Neural Density Models

**Authors:** Georg Ostrovski, Marc Bellemare, Aaron van den Oord, Remi Munos

Count-based exploration based on prediction gain of a simple graphical density model has previously achieved state-of-the-art results on some of the hardest exploration games in Atari. We investigate the open questions 1) whether a better density model leads to better exploration, and 2) what role the mixed Monte Carlo update rule used in this work plays for exploration. We show that a neural density model - PixelCNN - can be trained online on the experience stream of an RL agent and used for count-based exploration to achieve even better results on a wider set of hard exploration games, while preserving higher performance on easy exploration games. We also show that the Monte Carlo return is crucial in making use of the intrinsic reward signal in the sparsest reward settings, and cannot easily be replaced by a softer lambda-return update rule.

For further details and related work, please see the [paper](https://arxiv.org/abs/1703.01310).

**Check it out at ICML:**

Wednesday 09 August, 13:30-13:48 @ C4.5 (Talk)

Wednesday 09 August, 18:30-22:00 @ Gallery #64 (Poster)

## The Predictron: End-to-End Learning and Planning

**Authors:** David Silver, Hado van Hasselt, Matteo Hessel, Tom Schaul, Arthur Guez, Tim Harley, Gabriel Dulac-Arnold, David Reichert, Neil Rabinowitz, Andre Barreto, Thomas Degris

One of the key challenges of artificial intelligence is to learn models that are effective in the context of planning. In this document we introduce the predictron architecture. The predictron consists of a fully abstract model, represented by a Markov reward process, that can be rolled forward multiple “imagined" planning steps. Each forward pass of the predictron accumulates internal rewards and values over multiple planning depths. The predictron is trained end-to-end so as to make these accumulated values accurately approximate the true value function. We applied the predictron to procedurally generated random mazes and a simulator for the game of pool. The predictron yielded significantly more accurate predictions than conventional deep neural network architectures.

For further details and related work, please see the [paper](https://arxiv.org/abs/1612.08810).

**Check it out at ICML:**

Wednesday 09 August, 14:24-14:42 @ C4.5 (Talk)

Wednesday 09 August 18:30-20:00 @ Gallery #91 (Poster)

## FeUdal Networks for Hierarchical Reinforcement Learning

**Authors:** Sasha Vezhnevets, Simon Osindero, Tom Schaul, Nicolas Hees, Max Jaderberg, David Silver, Koray Kavukcuoglu

How to create agents that can learn to decompose their behaviour into meaningful primitives and then reuse them to more efficiently acquire new behaviours is a long standing research question. The solution to this question may be an important stepping stone towards agents with general intelligence and competence. This paper introduced FeUdal Networks (FuN), a novel architecture that formulates sub-goals as directions in latent state space, which, if followed, translates into a meaningful behavioural primitives. FuN clearly separates the module that discovers and sets sub-goals from the module that generates behaviour through primitive actions. This creates a natural hierarchy that is stable and allows both modules to learn in complementary ways. Our experiments clearly demonstrate that this makes long-term credit assignment and memorisation more tractable. This also opens many avenues for further research, for instance: deeper hierarchies can be constructed by setting goals at multiple time scales, scaling agents to truly large environments with sparse rewards and partial observability.

For further details and related work, please see the [paper](https://arxiv.org/abs/1703.01161).

**Check it out at ICML:**

Wednesday 09 August, 15:30-15:48 @ C4.5 (Talk)

Wednesday 09 August, 18:30-20:00 @ Gallery #107 (Poster)

## Neural Episodic Control

**Authors:** Alex Pritzel, Benigno Uria, Sriram Srinivasan, Adria Puigdomenech, Oriol Vinyals, Demis Hassabis, Daan Wierstra, Charles Blundell

Deep reinforcement learning algorithms have achieved state of the art performance on a variety of tasks, however they tend to be grossly data inefficient. In this work we propose a novel algorithm that allows rapid incorporation of new information collected by the agent. For this we introduce a new differentiable data structure, a differentiable neural dictionary, that can incorporate new information immediately, while being able to update it’s internal representation based on the task the algorithm is supposed to solve. Our agent, Neural Episodic Control, is built on top of the differentiable data structure and is able to learn significantly faster across a wide range of environments.

For further details and related work, please see the [paper](https://arxiv.org/pdf/1703.01988.pdf).

**Check it out at ICML:**

Wednesday 09 August, 16:06-16:24 @ C4.5

Wednesday 09 August, 18:30-22:00 @ Gallery #125

## Neural Message Passing Learns Quantum Chemistry

**Authors:** Justin Gilmer (Google Brain), Sam Schoenholz (Google Brain), Patrick Riley (Google Google), Oriol Vinyals, George Dahl (Google Brain)

In this work we show how we can gain orders of magnitude improvements to run-time performance by treating an expensive simulation of quantum chemistry properties as a supervised dataset to be learnt by extending neural networks to operate on graphs. Our model is extremely accurate and very fast. In the manuscript we also provide a unifying framework which summarises previous work on graph-shaped inputs and neural networks.

For further details and related work, please see the [paper](https://arxiv.org/abs/1704.01212).

**Check it out at ICML:**

Wednesday 09 August, 16:24-16:42 @ Darling Harbour Theatre (Talk)

Wednesday 09 August, 18:30-22:00 @ Gallery #131 (Poster)
