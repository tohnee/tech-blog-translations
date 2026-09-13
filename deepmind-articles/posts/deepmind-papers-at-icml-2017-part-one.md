---
title: "DeepMind papers at ICML 2017 (part one)"
source: https://deepmind.google/blog/deepmind-papers-at-icml-2017-part-one/
site: deepmind
date: 2017-08-04
authors: 
crawled: 2026-09-13
---

The first of our three-part series, which gives brief descriptions of the papers we are presenting at the ICML 2017 Conference in Sydney, Australia.

## Decoupled Neural Interfaces using Synthetic Gradients

**Authors:** Max Jaderberg, Wojciech Marian Czarnecki, Simon Osindero, Oriol Vinyals, Alex Graves, David Silver, Koray Kavukcuoglu

When training neural networks, the modules (layers) are locked: they can only be updated after backpropagation. We remove this constraint by incorporating a learnt model of error gradients, Synthetic Gradients, which means we can update networks without full backpropagation. We show how this can be applied to feed-forward networks which allows every layer to be trained asynchronously, to RNNs which extends the time over which models can remember, and to multi-network systems to allow communication.

For further details and related work, please see the [paper](https://arxiv.org/abs/1608.05343).

**Check it out at ICML:**

Monday 07 August, 10:30-10:48 @ Darling Harbour Theatre (Talk)

Monday 07 August, 18:30-22:00 PM @ Gallery #1 (Poster)

## Parallel Multiscale Autoregressive Density Estimation

**Authors:** Scott Reed, Aäron van den Oord, Nal Kalchbrenner, Ziyu Wang, Dan Belov, Nando de Freitas

The parallel multiscale autoregressive density estimator generates high-resolution (512 by 512) images, with orders of magnitude speedup over other autoregressive models. We evaluate the model on class-conditional image generation, text-to-image synthesis, and action-conditional video generation, showing that our model achieves the best results among non-pixel-autoregressive density models that allow efficient sampling.

For further details and related work, please see the [paper](https://arxiv.org/abs/1703.03664).

**Check it out at ICML:**

Monday 07 August, 10:48-11:06 @ Parkside 1 (Talk)

Monday 07 August, 18:30-20:00 @ Gallery #10 (Poster)

## Understanding Synthetic Gradients and Decoupled Neural Interfaces

**Authors:** Wojtek Czarnecki, Grzegorz Świrszcz, Max Jaderberg, Simon Osindero, Oriol Vinyals, Koray Kavukcuoglu

Synthetic gradients has been shown to work empirically in both feed-forward and recurrent cases. This work focuses on why and how it actually works - it shows that under mild assumptions critical points are preserved and that in the simplest case of linear model, synthetic gradients based learning does converge to the global optimum. On the other hand, we present empirically that trained models might be qualitatively different from those obtained using backpropagation.

For further details and related work, please see the [paper](https://arxiv.org/abs/1703.00522).

**Check it out at ICML:**

Monday 07 August, 10:48-11:06 @ Darling Harbour Theatre (Talk)

Monday 07 August, 18:30-20:00 @ Gallery #9 (Poster)

## Minimax Regret Bounds for Reinforcement Learning

**Authors:** Mohammad Gheshlaghi Azar, Ian Osband, Remi Munos

We consider the problem of provably optimal exploration in reinforcement learning for finite horizon MDPs. We show that an optimistic modification to value iteration achieves a regret bound of order (HSAT)1/2 (up to a logarithmic factor) where H is the time horizon, S the number of states, A the number of actions and T the number of time-steps. This result improves over the best previous known bound HS(AT)1/2 achieved by the UCRL2 algorithm of [Jaksch, Ortner, Auer, 2010]. The key significance of our new results is that for large T, the sample complexity of our algorithm matches the optimal lower bound of Ω(HSAT)1/2. Our analysis contains two key insights. We use careful application of concentration inequalities to the optimal value function as a whole, rather than to the transitions probabilities (to improve scaling in S), and we define Bernstein-based "exploration bonuses" that use the empirical variance of the estimated values at the next states (to improve scaling in H).

For further details and related work, please see the [paper](https://arxiv.org/abs/1703.05449).

**Check it out at ICML:**

Monday 07 August, 10:48-11:06 @ C4.5 (Talk)

Monday 07 August, 18:30-22:00 @ Gallery #12 (Poster)

## Video Pixel Networks

**Authors:** Nal Kalchbrenner, Aaron van den Oord, Karen Simonyan, Ivo Danihelka, Oriol Vinyals,Alex Graves, Koray Kavukcuoglu

Predicting the continuation of frames in a video is a hallmark task in unsupervised learning. We present a video model, the VPN, that is probabilistic and that is able to make accurate and sharp predictions of future video frames. The VPN achieves, for the first time, a nearly perfect score on the Moving MNIST dataset and produces plausible futures of up to 18 frames of robotic arm movements.

For further details and related work, please see the [paper](https://arxiv.org/abs/1610.00527).

**Check it out at ICML:**

Monday 07 August, 11:06-11:24 @ Parkside 1 (Talk)

Monday 07 August, 18:30-22:00 @ Gallery #18 (Poster)

## Sharp Minima Can Generalize For Deep Nets

**Authors:** Laurent Dinh (Univ. Montreal), Razvan Pascanu, Samy Bengio (Google Brain), Yoshua Bengio (Univ. Montreal)

Empirically, it has been observed that deep networks generalise well, even when they have the capacity to overfit the data. Additionally, it seems that stochastic gradient descent results in models that generalise better than batch method. One hypothesis for explaining this phenomena is that the noise of SGD helps model to find wide minina which generalise better than sharp (narrow) minima. In this work we try to improve our understanding of this hypothesis. We show that it does not hold for proposed definitions of wideness or sharpness due to the structure of neural networks. This suggest that there is no causality connection between batchsize size and generalisation.

For further details and related work, please see the [paper](https://arxiv.org/abs/1703.04933).

**Check it out at ICML:**

Monday 07 August, 11:06-11:24 @ C4.8 (Talk)

Tuesday 08 August, 18:30-22:00 @ Gallery #3 (Poster)
