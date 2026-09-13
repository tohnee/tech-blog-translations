---
title: "DeepMind papers at NIPS 2017"
source: https://deepmind.google/blog/deepmind-papers-at-nips-2017/
site: deepmind
date: 2017-12-01
authors: 
crawled: 2026-09-13
---

Between 04-09 December, thousands of researchers and experts will gather for the Thirty-first Annual Conference on [Neural Information Processing Systems](https://nips.cc/) (NIPS) in Long Beach, California.

Here you will find an overview of the papers DeepMind researchers will present.


### Robust imitation of diverse behaviours

**Authors:** Ziyu Wang, Josh Merel, Greg Wayne, Nando de Freitas, Scott Reed, Nicolas Heess

“We propose a neural network architecture, building on state-of-the-art generative models, that is capable of learning the relationships between different behaviours and imitating specific actions that it is shown. After training, our system can encode a single observed action and create a new novel movement based on that demonstration. It can also switch between different kinds of behaviours despite never having seen transitions between them, for example switching between walking styles.” Read more on [the blog](https://deepmind.com/blog/article/producing-flexible-behaviours-simulated-environments)

- Read the [paper](https://arxiv.org/abs/1707.02747)
- Check out the **poster** at **Pacific Ballroom #143** from **1830-2230**

### Sobolev training for neural networks

**Authors:** Wojtek Czarnecki, Simon Osindero, Max Jaderberg, Grzegorz Świrszcz, Razvan Pascanu

This paper shows a simple way of incorporating knowledge about target function derivatives into the training of deep neural networks. We prove that modern ReLU-based architectures are well suited for such tasks, and evaluate their effectiveness on three problems - low-dimensional regression, policy distillation, and training with synthetic gradients. We observe a significant boost in training efficiency, especially in low-data regimes, and train the first synthetic gradient-based ImageNet model with near state-of-the-art accuracy.

- Read the [paper](https://arxiv.org/abs/1706.04859)
- Check out the **poster** at **Pacific Ballroom #139** from **1830-2230**


### Filtering variational objectives

**Authors:** Chris J. Maddison, Dieterich Lawson, George Tucker, Nicolas Heess, Mohammad Norouzi, Andriy Mnih, Arnaud Doucet, Yee Whye Teh

We consider the extension of the variational lower bound to a family of lower bounds defined by a particle filter's estimator of the marginal likelihood - the filtering variational objectives. These filtering objectives can exploit a model's sequential structure to form tighter bounds and better objectives for model learning in deep generative models. In our experiments, we find that training with filtering objectives results in substantial improvements over training the same model architecture with the variational lower bound.

- Read the [paper](https://arxiv.org/abs/1705.09279)
- Check out the **poster** at **Pacific Ballroom #114** from **1830-2230**

### Visual interaction networks: Learning a physics simulator from video

**Authors:** Nicholas Watters, Andrea Tacchetti, Theophane Weber, Razvan Pascanu, Peter Battaglia, Daniel Zoran

“In this work we developed the “Visual Interaction Network” (VIN), a neural network-based model that learns physical dynamics without prior knowledge. The VIN is able to infer the states of multiple physical objects from just a few frames of video, and then use these to predict object positions many steps into the future. It is also able to infer the locations of invisible objects and learn dynamics that depend on object attributes such as mass.” Read [the blog](https://deepmind.com/blog/article/neural-approach-relational-reasoning) for further detail.

- Read the [paper](https://arxiv.org/abs/1706.01433)
- Check out the **poster** at **Pacific Ballroom #123** from **1830-2230**

### Neural discrete representation learning

**Authors:** Aäron van den Oord, Oriol Vinyals, Koray Kavukcuoglu

Learning useful representations without supervision remains a key challenge in machine learning. In this work we propose a simple yet powerful generative model - known as the Vector Quantised Variational AutoEconder (VQ-VAE) - that learns such discrete representations. When these representations are paired with an autoregressive prior, the model is able to generate high quality images, videos and speech as well as doing high-quality speaker conversion.

- Read the [paper](https://arxiv.org/abs/1711.00937)
- Check out the **poster** at **Pacific Ballroom #116** from **1830-2230**

### Variational memory addressing in generative models

**Authors:** Jörg Bornschein, Andriy Mnih, Daniel Zoran, Danilo Jimenez Rezende

Attention based memory can be used to augment neural networks to support few-shot learning, rapid adaptability and more generally to support non-parametric extensions. Instead of using the popular differentiable soft-attention mechanism, we propose the use of stochastic hard-attention to retrieve memory content in generative models. This allows us to apply variational inference to memory addressing, which enables us to get significantly more precise memory lookups using target information, especially in models with large memory buffers and with many confounding entries in the memory.

- Read the [paper](https://arxiv.org/abs/1709.07116)
- Check out the **poster** at **Pacific Ballroom #117** from **1830-2230**


### REBAR: Low-variance, unbiased gradient estimates for discrete latent variable models

**Authors:** George Tucker, Andriy Mnih, Chris J Maddison, Dieterich Lawson, Jascha Sohl-Dickstein

Learning in models with discrete latent variables is challenging due to high-variance gradient estimators. Previous approaches either produced high-variance, unbiased gradients or low-variance, biased gradients. REBAR uses control variates and the reparameterization trick to get the best of both: low-variance, unbiased gradients that result in faster convergence to a better result.

- Read the [paper](https://arxiv.org/abs/1703.07370)
- Attend the **oral** session in **Hall A** from **1035-1050**
- Check out the **poster** at **Pacific Ballroom #178** from **0630-2230**

### Imagination-augmented agents for deep reinforcement learning

**Authors:** Sébastien Racanière, Théophane Weber, David P. Reichert, Lars Buesing, Arthur Guez, Danilo Rezende, Adria Puigdomènech Badia, Oriol Vinyals, Nicolas Heess, Yujia Li, Razvan Pascanu, Peter Battaglia, Demis Hassabis, David Silver, Daan Wierstra.

“We describe a new family of approaches for imagination-based planning...We also introduce architectures which provide new ways for agents to learn and construct plans to maximise the efficiency of a task. These architectures are efficient, robust to complex and imperfect models, and can adopt flexible strategies for exploiting their imagination. The agents we introduce benefit from an ‘imagination encoder’- a neural network which learns to extract any information useful for the agent’s future decisions, but ignore that which is not relevant.” Read more on [the blog](https://deepmind.com/blog/article/agents-imagine-and-plan).

- Read the [paper](https://arxiv.org/abs/1707.06203)
- Attend the **oral** session in **Hall A** from **1505-1520**
- Check out the **poster** at **Pacific Ballroom #139** from **1830-2230**

### A simple neural network module for relational reasoning

**Authors:** Adam Santoro, David Raposo, David Barrett, Mateusz Malinowski, Razvan Pascanu, Peter Battaglia, Timothy Lillicrap

“We demonstrate the use of a simple, plug-and-play neural network module for solving tasks that demand complex relational reasoning. This module, called a Relation Network, can receive unstructured inputs - say, images or stories - and implicitly reason about the relations contained within.” Read more on [the blog](https://deepmind.com/blog/article/neural-approach-relational-reasoning).

- Read the [paper](https://arxiv.org/abs/1706.01427)
- Listen to the **spotlight** talk in **Hall A** from **1525-1530**
- Check out the **poster** at **Pacific Ballroom #129** from **1830-2230**

### Simple and scalable predictive uncertainty estimation using deep ensembles

**Authors:** Balaji Lakshminarayanan, Alexander Pritzel, Charles Blundell

Quantifying predictive uncertainty in neural networks (NNs) is a challenging and yet unsolved problem. The majority of work is focused on Bayesian solutions, however these are computationally intensive and require significant modifications to the training pipeline. We propose an alternative to Bayesian NNs that is simple to implement, readily parallelisable, requires very little hyperparameter tuning, and yields high quality predictive uncertainty estimates. Through a series of experiments on classification and regression benchmarks, we demonstrate that our method produces well-calibrated uncertainty estimates which are as good or better than approximate Bayesian NNs.

- Read the [paper](https://arxiv.org/abs/1612.01474)
- Listen to the **spotlight** talk in **Hall A** from **1545-1550**
- Check out the **poster** at **Pacific Ballroom #133** from **1830-2230**

### Natural value approximators: learning when to trust past estimates

**Authors:** Zhongwen Xu, Joseph Modayil, Hado van Hasselt, Andre Barreto, David Silver, Tom Schaul

We revisit the structure of value approximators for RL, based on the observation that typical approximators smoothly change as a function of input, but the true value changes abruptly when a reward arrives. Our proposed method is designed to fit such asymmetric discontinuities using interpolation with a projected value estimate.

- Read the [paper](http://papers.nips.cc/paper/6807-natural-value-approximators-learning-when-to-trust-past-estimates)
- Listen to the **spotlight** talk in **Hall A** from **1725-1730**
- Check out the **poster** at **Pacific Ballroom #6** from **1830-2230**

### Successor features for transfer in reinforcement learning

**Authors:** Andre Barreto, Will Dabney, Remi Munos, Jonathan Hunt, Tom Schaul, David Silver, Hado van Hasselt.

We propose a transfer framework for reinforcement learning. Our approach rests on two key ideas: "successor features", a value function representation that decouples the dynamics of the environment from the rewards, and "generalised policy improvement", a generalisation of dynamic programming’s policy improvement step that considers a set of policies rather than a single one. Put together, the two ideas lead to an approach that integrates seamlessly within the reinforcement learning framework and allows transfer to take place between tasks without any restriction.

- Read the [paper](https://arxiv.org/abs/1606.05312)
- Listen to the **spotlight** talk in **Hall A** from **1740-1745**
- Check out the **poster** at **Pacific Ballroom #9** from **1830-2230**

### Deep reinforcement learning from human preferences

**Authors:** Paul Christiano (Open AI), Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, Dario Amodei (Open AI)

“A central question in technical AI safety is how to tell an algorithm what we want it to do. Working with OpenAI, we demonstrate a novel system that allows a human with no technical experience to teach an AI how to perform a complex task, such as manipulating a simulated robotic arm.” Read more on [the blog](https://deepmind.com/blog/article/learning-through-human-feedback).

- Read the [paper](https://arxiv.org/abs/1706.03741)
- Check out the **poster** at **Pacific Ballroom #1** from **1830-2230**

### A multi-agent reinforcement learning model of common-pool resource appropriation

**Author:** Julien Perolat, Joel Z Leibo, Vinicius Zambaldi, Charles Beattie, Karl Tuyls, Thore Graepel

This paper looks at the complexity of problems of common-pool resource appropriation. These include systems such as fisheries, grazing pastures or access to freshwater, where lots of people or actors have access to the same resource. Traditional models from the social sciences tend to suggest that parties with access to the resource act in a self-interested way, eventually leading to an unsustainable depletion of resources. However, we know from human societies that there is a wide range of possible outcomes. Sometimes resources like fisheries are overexploited and sometimes they are harvested sustainably. In this work we propose new modeling techniques that can be used in research aimed at explaining this gap between what we observe in the real world and what traditional models predict.

- Read the [paper](https://arxiv.org/abs/1707.06600)
- Check out the **poster** at **Pacific Ballroom #86** from **1830-2230**

### DisTraL: Robust multitask reinforcement learning

**Authors:** Yee Whye Teh, Victor Bapst, Wojciech Czarnecki, John Quan, James Kirkpatrick, Raia Hadsell, Nicholas Heess, Razvan Pascanu

We develop a method for doing reinforcement learning on multiple tasks. The assumption is that the tasks are related to each other (e.g. being in the same environment or having the same physics) and so good action sequences tend to recur across tasks. Our method achieves this by simultaneously distilling task-specific policies into a common default policy, and transferring this common knowledge across tasks by regularising all task-specific policies towards the default policy. We show that this leads to faster and more robust learning.

- Read the [paper](https://arxiv.org/abs/1707.04175)
- Check out the **poster** at **Pacific Ballroom #138** from **1830-2230**

### A unified game-theoretic approach to multiagent reinforcement learning

**Authors:** Marc Lanctot, Vinicius Zambaldi, Audrunas Gruslys, Angeliki Lazaridou, Karl Tuyls, Julien Perolat, David Silver, Thore Graepel

In this work, we first observe that independent reinforcement learners produce policies that can be jointly correlated, failing to generalize well during execution with other agents. We quantify this effect by proposing a new metric called joint policy correlation. We then propose an algorithm motivated by game-theoretic foundations, which generalises several previous approaches such as fictitious play, iterated best response, independent RL, and double oracle. We show that our algorithm can reduce joint policy correlation significantly in first-person coordination games, and finds robust counter-strategies in a common poker benchmark game.

- Read the [paper](https://arxiv.org/abs/1711.00832)
- Check out the **poster** at **Pacific Ballroom #203** from **1830-2230**

Our researchers will also lead and take part in a wide-range of workshops, tutorials and symposia during NIPS. For the full schedule, including details of papers that we have collaborated on, please download our [itinerary](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/deepmind-papers-at-nips-2017/DeepMind_Itinerary_NIPS2017.pdf) (PDF) or visit [the official website](https://nips.cc/).
