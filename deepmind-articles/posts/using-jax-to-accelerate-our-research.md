---
title: "Using JAX to accelerate our research"
source: https://deepmind.google/blog/using-jax-to-accelerate-our-research/
site: deepmind
date: 2020-12-04
authors: David Budden, Matteo Hessel
crawled: 2026-09-13
---

DeepMind engineers accelerate our research by building tools, scaling up algorithms, and creating challenging virtual and physical worlds for training and testing artificial intelligence (AI) systems. As part of this work, we constantly evaluate new machine learning libraries and frameworks.

Recently, we've found that an increasing number of projects are well served by [JAX](https://github.com/google/jax#jax-autograd-and-xla-), a machine learning framework developed by [Google Research](https://research.google/) teams. JAX resonates well with our engineering philosophy and has been widely adopted by our research community over the last year. Here we share our experience of working with JAX, outline why we find it useful for our AI research, and give an overview of the ecosystem we are building to support researchers everywhere.

![The JAX logo, spelt out in blue, green, and purple 3D blocks.](https://lh3.googleusercontent.com/wBCIw9Mu04RHjWEB5A1To_jIHcnjpvyIRxsudBvcOhOfMJvs6KZElN62hlSxLmBdWFnwXdu3iiSFZcZkajS-F5vN89SJ8i55wxoEW6VpZvLEHC0nNR0=w1440)

## Why JAX?

JAX is a Python library designed for high-performance numerical computing, especially machine learning research. Its API for numerical functions is based on [NumPy](https://www.nature.com/articles/s41586-020-2649-2), a collection of functions used in scientific computing. Both Python and NumPy are widely used and familiar, making JAX simple, flexible, and easy to adopt.

In addition to its NumPy API, JAX includes an extensible system of composable function transformations that help support machine learning research, including:

- **Differentiation:** Gradient-based optimisation is fundamental to ML. JAX natively supports both forward and reverse mode [automatic differentiation](https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html) of arbitrary numerical functions, via function transformations such as grad, hessian, jacfwd and jacrev.
- **Vectorisation:** In ML research we often apply a single function to lots of data, e.g. calculating the loss across a batch or [evaluating per-example gradients](https://arxiv.org/abs/2010.09063) for differentially private learning. JAX provides automatic vectorisation via the vmap transformation that simplifies this form of programming. For example, researchers don't need to reason about batching when implementing new algorithms. JAX also supports large scale data parallelism via the related pmap transformation, elegantly distributing data that is too large for the memory of a single accelerator.
- **JIT-compilation:** [XLA](https://www.tensorflow.org/xla) is used to just-in-time (JIT)-compile and execute JAX programs on GPU and [Cloud TPU](https://cloud.google.com/tpu) accelerators. JIT-compilation, together with JAX's NumPy-consistent API, allows researchers with no previous experience in high-performance computing to easily scale to one or many accelerators.

We have found that JAX has enabled rapid experimentation with novel algorithms and architectures and it now underpins many of our recent publications. To learn more please consider joining our JAX Roundtable, Wednesday December 9th 7:00pm GMT, at the [NeurIPS](https://neurips.cc/) virtual conference.

## JAX at DeepMind

Supporting state-of-the-art AI research means balancing rapid prototyping and quick iteration with the ability to deploy experiments at a scale traditionally associated with production systems. What makes these kinds of projects particularly challenging is that the research landscape evolves rapidly and is difficult to forecast. At any point, a new research breakthrough may, and regularly does, change the trajectory and requirements of entire teams. Within this ever-changing landscape, a core responsibility of our engineering team is to make sure that the lessons learned and the code written for one research project is reused effectively in the next.

One approach that has proven successful is modularisation: we extract the most important and critical building blocks developed in each research project into well tested and efficient **components**. This empowers researchers to focus on their research while also benefiting from code reuse, bug fixes and performance improvements in the algorithmic ingredients implemented by our core libraries. We’ve also found that it’s important to make sure that each library has a clearly defined scope and to ensure that they’re interoperable but independent. **Incremental buy-in**, the ability to pick and choose features without being locked into others, is critical to providing maximum flexibility for researchers and always supporting them in choosing the right tool for the job.

Other considerations that have gone into the development of our JAX Ecosystem include making sure that it remains consistent (where possible) with the design of our existing [TensorFlow](https://www.tensorflow.org/guide) libraries (e.g. [Sonnet](https://deepmind.com/blog/article/open-sourcing-sonnet) and [TRFL](https://deepmind.com/blog/article/trfl)). We’ve also aimed to build components that (where relevant) match their underlying mathematics as closely as possible, to be self-descriptive and minimise mental hops "from paper to code". Finally, we’ve chosen to [open source](https://github.com/deepmind) our libraries to facilitate sharing of research outputs and to encourage the broader community to explore the JAX Ecosystem.


## Haiku

![An animated page of code.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277dc798849b366fe787ef_Haiku.gif)

The JAX programming model of composable function transformations can make dealing with stateful objects complicated, e.g. neural networks with trainable parameters. Haiku is a neural network library that allows users to use familiar object-oriented programming models while harnessing the power and simplicity of JAX's pure functional paradigm.

Haiku is actively used by hundreds of researchers across DeepMind and Google, and has already found adoption in several external projects (e.g. [Coax](https://github.com/microsoft/coax), [DeepChem](https://github.com/deepchem/jaxchem), [NumPyro](https://github.com/pyro-ppl/numpyro/blob/master/numpyro/contrib/module.py)). It builds on the API for [Sonnet](https://github.com/deepmind/sonnet), our module-based programming model for neural networks in TensorFlow, and we’ve aimed to make porting from Sonnet to Haiku as simple as possible.

[**Find out more on GitHub**](https://github.com/deepmind/dm-haiku)

## Optax

![An animated page of code.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277de6e5d933b07c0a6039_Optax.gif)

Gradient-based optimisation is fundamental to ML. Optax provides a library of gradient transformations, together with composition operators (e.g. chain) that allow implementing many standard optimisers (e.g. RMSProp or Adam) in just a single line of code.

The compositional nature of Optax naturally supports recombining the same basic ingredients in custom optimisers. It additionally offers a number of utilities for stochastic gradient estimation and second order optimisation.

Many Optax users have adopted Haiku but in line with our incremental buy-in philosophy, any library representing parameters as JAX tree structures is supported (e.g. [Elegy](https://github.com/poets-ai/elegy), [Flax](https://github.com/google/flax) and [Stax](https://jax.readthedocs.io/en/latest/jax.experimental.stax.html)). Please see [here](https://github.com/google/jax#neural-network-libraries) for more information on this rich ecosystem of JAX libraries.

[**Find out more on GitHub**](https://github.com/deepmind/optax)

## RLax

![An animated page of code.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277e08098cb3c9c586e2f2_RLax.gif)

Many of our most successful projects are at the intersection of deep learning and reinforcement learning (RL), also known as [deep reinforcement learning](https://deepmind.com/blog/article/deep-reinforcement-learning). RLax is a library that provides useful building blocks for constructing RL agents.

The components in RLax cover a broad spectrum of algorithms and ideas: TD-learning, policy gradients, actor critics, MAP, proximal policy optimisation, non-linear value transformation, general value functions, and a number of exploration methods.

Although some introductory [example agents](https://github.com/deepmind/rlax/tree/master/examples) are provided, RLax is not intended as a framework for building and deploying full RL agent systems. One example of a fully-featured agent framework that builds upon RLax components is [Acme](https://deepmind.com/research/publications/Acme).

[**Find out more on GitHub**](https://github.com/deepmind/rlax)

## Chex

![An animated page of code.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277e21a0b933fa2006f5cd_Chex.gif)

Testing is critical to software reliability and research code is no exception. Drawing scientific conclusions from research experiments requires being confident in the correctness of your code. Chex is a collection of testing utilities used by library authors to verify the common building blocks are correct and robust and by end-users to check their experimental code.

Chex provides an assortment of utilities including JAX-aware unit testing, assertions of properties of JAX datatypes, mocks and fakes, and multi-device test environments. Chex is used throughout DeepMind’s JAX Ecosystem and by external projects such as [Coax](https://github.com/microsoft/coax) and [MineRL](https://github.com/dzorlu/minerl).

[**Find out more on GitHub**](https://github.com/deepmind/chex)

## Jraph

![An animated page of code.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277e3aa0b933afca071647_Jraph.gif)

[Graph neural networks](https://arxiv.org/abs/1806.01261) (GNNs) are an exciting area of research with many promising applications. See, for instance, our recent work on [traffic prediction](https://deepmind.com/blog/article/traffic-prediction-with-advanced-graph-neural-networks) in Google Maps and our work on [physics simulation](https://www.youtube.com/watch?v=2Bw5f4vYL98). Jraph (pronounced "giraffe") is a lightweight library to support working with GNNs in JAX.

Jraph provides a standardised data structure for graphs, a set of utilities for working with graphs, and a 'zoo' of easily forkable and extensible graph neural network models. Other key features include: batching of GraphTuples that efficiently leverage hardware accelerators, JIT-compilation support of variable-shaped graphs via padding and masking, and losses defined over input partitions. Like Optax and our other libraries, Jraph places no constraints on the user's choice of a neural network library.

Learn more about using the library from our rich collection of [examples](https://github.com/deepmind/jraph/tree/master/jraph/examples).

[**Find out more on GitHub**](https://github.com/deepmind/jraph)

Our JAX Ecosystem is constantly evolving and we encourage the ML research community to explore [our libraries](https://deepmind.com/research?filters=%7B%22collection%22:%5B%22OpenSource%22%5D%7D) and the potential of JAX to accelerate their own research.

**Citing the DeepMind JAX Ecosystem**

If you find the DeepMind JAX Ecosystem useful for your work, please use [this citation](https://github.com/deepmind/jax/blob/main/deepmind2020jax.txt) (hosted on GitHub).
