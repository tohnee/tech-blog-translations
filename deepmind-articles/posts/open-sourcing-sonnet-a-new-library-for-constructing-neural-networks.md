---
title: "Open sourcing Sonnet - a new library for constructing neural networks"
source: https://deepmind.google/blog/open-sourcing-sonnet-a-new-library-for-constructing-neural-networks/
site: deepmind
date: 2017-04-07
authors: Malcolm Reynolds, Jack Rae, Andreas Fidjeland, Fabio Viola, Adrià Puigdomènech, Frederic Besse, Tim Green, Sébastien Racanière, Gabriel Barth-Maron, Diego de Las Casas
crawled: 2026-09-13
---

It’s now nearly a year since DeepMind [made the decision to switch the entire research organisation to using TensorFlow (TF)](https://ai.googleblog.com/2016/04/deepmind-moves-to-tensorflow.html). It’s proven to be a good choice - many of our models learn significantly faster, and the built-in features for distributed training have hugely simplified our code. Along the way, we found that the flexibility and adaptiveness of TF lends itself to building higher level frameworks for specific purposes, and we’ve written one for quickly building neural network modules with TF. We are actively developing this codebase, but what we have so far fits our research needs well, and we’re excited to announce that today we are open sourcing it. We call this framework [Sonnet](https://github.com/deepmind/sonnet).

Since its initial launch in November 2015, a diverse ecosystem of higher level libraries has sprung up around [TensorFlow](https://www.tensorflow.org/) enabling common tasks to be accomplished quicker. Sonnet shares many similarities with some of these existing neural network libraries, but has some features specifically designed around our research requirements. The [code release](https://github.com/deepmind/learning-to-learn) accompanying our [Learning to learn paper](https://arxiv.org/abs/1606.04474) included a preliminary version of Sonnet, and other forthcoming code releases will be built on top of the full library we are releasing today.

Making Sonnet public allows other models created within DeepMind to be easily shared with the community, and we also hope that the community will use Sonnet to take their own research forwards. In recent months we’ve also open-sourced our flagship platform [DeepMind Lab](https://deepmind.google/research/), and are currently working with [Blizzard to develop an open source API that supports AI research in StarCraft II](https://deepmind.com/blog/announcements/deepmind-and-blizzard-release-starcraft-ii-ai-research-environment). There are many more releases to come, and they’ll all be shared on our new [Open Source page](https://deepmind.com/research?filters=%7B%22collection%22:%5B%22OpenSource%22%5D%7D).

The library uses an object-oriented approach, similar to Torch/NN, allowing modules to be created which define the forward pass of some computation. Modules are ‘called’ with some input Tensors, which adds ops to the Graph and returns output Tensors. One of the design choices was to make sure the variable sharing is handled transparently by automatically reusing variables on subsequent calls to the same module.

Many models in the literature can naturally be considered as a hierarchy - e.g. a Differentiable Neural Computer contains a controller which might be an LSTM, which can be implemented as containing a standard Linear layer. We’ve found that writing code which explicitly represents submodules allows easy code reuse and quick experimentation - Sonnet promotes writing modules which declare other submodules internally, or are passed other modules at construction time.

![Sonnet logo.](https://lh3.googleusercontent.com/oq_ck82hUcoq8aOt0HqEoPEoMN0jbcIMUY2ifRM8gvJq2GhUjhJLYTpne1xYOcEw0hJXRn6I73mh8KybKVOuWZhrgx3hqhs3cjMvVHTBtd9c8HKfUyk=w1440)

A final technique we’ve found very useful is to allow certain modules to operate on arbitrarily nested groups of Tensors. Recurrent Neural Network states are often best represented as a collection of heterogeneous Tensors, and representing these as a flat list can be error prone. Sonnet provides utilities to deal with these arbitrary hierarchies, so that changing your experiment to use a different kind of RNN does not require tedious code changes. We’ve made changes to core TF as well to better support this use case.

Sonnet is designed specifically to work with TensorFlow, and as such does not prevent you from accessing the underlying details such as Tensors and variable\_scopes. Models written in Sonnet can be freely mixed with raw TF code, and that in other high level libraries.

This is not a one-time release - we will regularly update the Github repository to match our in-house version. We’ve got lots of ideas for new features in the works, which will be made available when ready. We are very excited about contributions from the community.

**Notes**

View Sonnet on [Github](http://www.github.com/deepmind/sonnet)
